// -!- c++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Mon Feb 6 09:47:06 2023
//  Last Modified : <231109.0955>
//
//  Description	
//
//  Notes
//
//  History
//	
/////////////////////////////////////////////////////////////////////////////
//
//    Copyright (C) 2023  Robert Heller D/B/A Deepwoods Software
//			51 Locke Hill Road
//			Wendell, MA 01379-9728
//
//    This program is free software; you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation; either version 2 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program; if not, write to the Free Software
//    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
//
// 
//
//////////////////////////////////////////////////////////////////////////////

#ifndef __SEQUENCE_HXX
#define __SEQUENCE_HXX

#include "openlcb/EventHandlerTemplates.hxx"
#include "openlcb/ConfigRepresentation.hxx"
#include "utils/ConfigUpdateListener.hxx"
#include "utils/ConfigUpdateService.hxx"
#include "utils/Uninitialized.hxx"
#include "openlcb/RefreshLoop.hxx"
#include "openlcb/SimpleStack.hxx"
#include "executor/Timer.hxx"
#include "executor/Notifiable.hxx"
#include <stdio.h>
#include <stdlib.h>
#include "utils/logging.h"
#include <string>
#include "OutputConfigGroup.hxx"
#include "StepConfigGroup.hxx"
#include "SequenceConfigGroup.hxx"
#include <freertos_drivers/esp32/Esp32Ledc.hxx>

extern PWM* const pwmchannels[];

#define BRIGHNESSHUNDRETHSPERCENT(b) ((b)*.0001)

class Output : public ConfigUpdateListener, public Timer {
public:
    enum OutputID : uint8_t {Unused, Buffer1_, Buffer2_, Buffer3_, Buffer4_, Buffer5_, 
              Buffer6_, Buffer7_, Buffer8_};
    enum OutputMode : uint8_t {On, Off, FadeOn, FadeOff, Flicker};
    Output(const OutputConfig &cfg, ActiveTimers *timers) 
                : Timer(timers)
          ,cfg_(cfg)
    {
        running_ = false;
        outputid_ = Unused;
        mode_ = Off;
        brightness_ = 5000;
        currentbrightness_ = 0;
        currentstate_ = off;
        ConfigUpdateService::instance()->register_update_listener(this);
    }
    void factory_reset(int fd) OVERRIDE
    {
        CDI_FACTORY_RESET(cfg_.selection);
        CDI_FACTORY_RESET(cfg_.mode);
        CDI_FACTORY_RESET(cfg_.brightness);
    }
    virtual UpdateAction apply_configuration(int fd,
                                             bool initial_load,
                                             BarrierNotifiable *done) override
    {
        AutoNotify n(done);
        outputid_ = (OutputID) cfg_.selection().read(fd);
        //if (outputid_ > Buffer8_) outputid_ = Unused;
        mode_ = (OutputMode) cfg_.mode().read(fd);
        //if (mode_ > Flicker) mode_ = Off;
        brightness_ = cfg_.brightness().read(fd);
        return UPDATED;
    }
    PWM* Pin() const       {return pinlookup_[(int)outputid_];}
    const OutputMode Mode() const {return mode_;}
    static PWM* PinLookup(OutputID id) 
    {
        return pinlookup_[(int)id];
    }
    void StartOutput()
    {
        if (outputid_ == Unused) return;
        PWM * p = Pin();
        if (p == nullptr) return;
        //LOG(INFO,"[Output::StartOutput] p = %p, mode_ = %d",p,mode_);
        switch (mode_)
        {
        case On:
            currentbrightness_ = brightness_;
            currentstate_ = on;
            break;
        case Off:
            currentbrightness_ = 0;
            currentstate_ = off;
            break;
        case FadeOn:
            if (currentstate_ != fadeup && currentbrightness_ < brightness_)
            {
                currentstate_ = fadeup;
                startDelay(500*1000000ULL); // 500ms
            }
            break;
        case FadeOff:
            if (currentstate_ != fadedown && currentbrightness_ > 0)
            {
                currentstate_ = fadedown;
                startDelay(500*1000000ULL); // 500ms
            }
            break;
        case Flicker:
            if (currentstate_ != flickering)
            {
                currentstate_ = flickering;
                currentbrightness_ = ((rand()&0x01FF)+128)*10;
                startDelay(((rand()&0x01FF)+128)*1000000ULL); // random 128-640 ms
            }
            break;
        }
        uint32_t duty = (uint32_t)(BRIGHNESSHUNDRETHSPERCENT(currentbrightness_)*p->get_period());
        //LOG(INFO,"[Output::StartOutput] duty = %lu",duty);
        p->set_duty(duty);
        //LOG(INFO,"[Output::StartOutput] p->get_duty() returns %lu", p->get_duty());
    }
    void log_duty()
    {
        if (outputid_ == Unused) return;
        PWM * p = Pin();
        if (p == nullptr) return;
        //LOG(INFO,"[Output::log_duty] p->get_duty() returns %lu", p->get_duty());
    }
    static void PinLookupInit(openmrn_arduino::Esp32Ledc &ledc,
                              int ostart = 0,int pstart = 0,
                              int count = OUTPUTCOUNT)
    {
        pinlookup_[(uint8_t)Unused] = nullptr;
        for (int i=0;i < count; i++)
        {
            int o=i+ostart;
            if (o > OUTPUTCOUNT) break;
            int p=i+pstart;
            if (p > LEDC_CHANNEL_MAX) break;
            pinlookup_[o+1] = ledc.get_channel(p);
        }
    }
    void StopFlicker()
    {
        if (running_)
        {
            currentstate_ = off;
        }
        else
        {
            if (outputid_ == Unused) return;
            PWM * p = Pin();
            if (p == nullptr) return;
            currentstate_ = off;
            currentbrightness_ = 0;
            p->set_duty((uint32_t)(BRIGHNESSHUNDRETHSPERCENT(currentbrightness_)*p->get_period()));
        }
    }
private:
    void startDelay(long long time) {
        if (running_) {
            return;
        }
        start(time);
        running_ = true;
    }
    long long timeout() override
    {
        running_ = false;
        if (outputid_ == Unused) return NONE;
        PWM * p = Pin();
        if (p == nullptr) return NONE; 
        switch (currentstate_)
        {
        case fadeup:
            if (currentbrightness_ < brightness_)
            {
                currentbrightness_ += 50;
                if (currentbrightness_ > brightness_) 
                {
                    currentbrightness_ = brightness_;
                }
                p->set_duty((uint32_t)(BRIGHNESSHUNDRETHSPERCENT(currentbrightness_)*p->get_period()));
                if (currentbrightness_ < brightness_)
                {
                    running_ = true;
                    return 500*1000000ULL; // 500ms
                }
                else
                {
                    currentstate_ = on;
                    return NONE;
                }
            }
            else
            {
                currentstate_ = on;
                return NONE;
            }
            break;
        case fadedown:
            if (currentbrightness_ > 0)
            {
                if (currentbrightness_ > 50)
                {
                    currentbrightness_ -= 50;
                }
                else
                {
                    currentbrightness_ = 0;
                }
                p->set_duty((uint32_t)(BRIGHNESSHUNDRETHSPERCENT(currentbrightness_)*p->get_period()));
                if (currentbrightness_ > 0)
                {
                    running_ = true;
                    return 500*1000000ULL; // 500ms
                }
                else
                {
                    currentstate_ = off;
                    return NONE;
                }
            }
            else
            {
                currentstate_ = off;
                return NONE;
            }
            break;
        case flickering:
            currentbrightness_ = ((rand()&0x01FF)+128)*10;
            p->set_duty((uint32_t)(BRIGHNESSHUNDRETHSPERCENT(currentbrightness_)*p->get_period()));
            running_ = true;
            return ((rand()&0x01FF)+128)*1000000ULL; // random 128-640ms
            break;
        case off:
            currentbrightness_ = 0;
            p->set_duty((uint32_t)(BRIGHNESSHUNDRETHSPERCENT(currentbrightness_)*p->get_period()));
            return NONE; 
            break;
        default:
            return NONE;
            break;
        }
        return NONE;
    }
    
            
    const OutputConfig cfg_;
    uint16_t brightness_;
    uint16_t currentbrightness_;
    OutputID outputid_;
    OutputMode mode_;
    enum OutputState : uint8_t {on, off, fadeup, fadedown, flickering} currentstate_;
    bool running_;
    static PWM* pinlookup_[OUTPUTCOUNT+1];
};

class Step;

class Sequence : public ConfigUpdateListener, 
                 public StateFlowBase, public openlcb::SimpleEventHandler 
{
public:
    Sequence(openlcb::Node *node, const SequenceConfig &cfg, Service *service)
                : StateFlowBase(service)
          , timer_(this)
          , cfg_(cfg)
          , node_(node)
    {
        enabled_ = false;
        start_ = 0ULL;
        stop_ = 0ULL; 
        stepRunning_ = false;
        running_ = false;
        stopped_ = true;
        for (int i = 0; i < STEPSCOUNT; i++)
        {
            steps_[i].emplace(node_,cfg_.steps().entry(i),service);
        }
        ConfigUpdateService::instance()->register_update_listener(this);
    }
    void factory_reset(int fd) OVERRIDE
    {
        cfg_.name().write(fd,"");
        CDI_FACTORY_RESET(cfg_.enabled);
    }
    UpdateAction apply_configuration(int fd, 
                                     bool initial_load,
                                     BarrierNotifiable *done) override
    {
        AutoNotify n(done);
        enabled_ = cfg_.enabled().read(fd);
        openlcb::EventId cfg_start = cfg_.start().read(fd);
        openlcb::EventId cfg_stop = cfg_.stop().read(fd);
        if (cfg_start != start_ || cfg_stop != stop_)
        {
            if (!initial_load)
            {
                unregister_handler();
            }
            start_ = cfg_start;
            stop_ = cfg_stop;
            register_handler();
            return REINIT_NEEDED; // Causes events identify. 
        }
        return UPDATED;
    }
    void handle_identify_global(const openlcb::EventRegistryEntry &registry_entry, 
                                openlcb::EventReport *event, BarrierNotifiable *done) override
    {
        if (event->dst_node && event->dst_node != node_)
        {
            done->notify();
            return;
        }
        SendAllConsumersIdentified(event,done);
        done->maybe_done(); 
    }
    void handle_identify_consumer(const openlcb::EventRegistryEntry &registry_entry,
                                  openlcb::EventReport *event,
                                  BarrierNotifiable *done) override
    {
        SendConsumerIdentified(event,done);
        done->maybe_done();
    }
    void handle_event_report(const openlcb::EventRegistryEntry &entry,
                             openlcb::EventReport *event,
                             BarrierNotifiable *done) override
    {
        AutoNotify n(done);
        if (event->event == stop_)
        {
            LOG(INFO,"[Sequence::handle_event_report] event->event == stop_");
            stopped_ = true;
            if (!running_) stopFlicker();
        }
        else
        {
            LOG(INFO,"[Sequence::handle_event_report] event->event == start_");
            if (running_) return;
            if (!enabled_) return;
            stopped_ = false;
            start_flow(STATE(entry));
        }
    }
    bool StopP()
    {
        return stopped_;
    }
private:
    Action entry()
    {
        running_ = true;
        istate_ = 0;
        return call_immediately(STATE(startStep));
    }
    Action startStep()
    {
        bn_.reset(this);
        SendEventReport(&write_helpers[0],steps_[istate_]->StartEventId());
        stepRunning_ = true;
        return sleep_and_call(&timer_,steps_[istate_]->StartStep(),STATE(endStep));
    }
    Action endStep()
    {
        steps_[istate_]->EndStep();
        SendEventReport(&write_helpers[1],steps_[istate_]->EndEventId());
        stepRunning_ = false;
        bn_.maybe_done();
        return wait_and_call(STATE(next));
    }
    Action next()
    {
        LOG(INFO,"[Sequence::next] stopped_ is %d",stopped_);
        if (stopped_)
        {
            return call_immediately(STATE(finish));
        }
        Step::NextMode_t next = steps_[istate_]->NextMode();
        switch (next)
        {
        case Step::NextMode_t::Last:  // This is the last step.
            return call_immediately(STATE(finish));
        case Step::NextMode_t::Next:  // Goto the next step in the list
            istate_++;
            if (istate_ < STEPSCOUNT)
            {
                return call_immediately(STATE(startStep));
            } 
            else
            {
                return call_immediately(STATE(finish));
            }
        case Step::NextMode_t::First: // Goto the first step (loop)
            istate_ = 0;
            return call_immediately(STATE(startStep));
        }
        // Should not get here.  This is only here to make the compiler happy.
        return exit();
    }
    Action finish()
    {
        stopped_ = true;
        running_ = false;
        stopFlicker();
        return exit();
    }

    void stopFlicker()
    {
        for (int istep = 0; istep < STEPSCOUNT; istep++)
        {
            steps_[istep]->StopFlicker();
        }
    }
    void SendEventReport(openlcb::WriteHelper *helper,openlcb::EventId event)
    {
        helper->WriteAsync(node_,
                           openlcb::Defs::MTI_EVENT_REPORT,
                           openlcb::WriteHelper::global(),
                           openlcb::eventid_to_buffer(event),
                           bn_.new_child());
    }
    class Step : public ConfigUpdateListener, 
          public openlcb::SimpleEventHandler 
    {
    public:
        enum NextMode_t : uint8_t {Last, Next, First};
        Step(openlcb::Node *node, const StepConfig &cfg, Service *service)
                    : cfg_(cfg)
              , node_(node)
        {
            nextMode_ = Last;
            time_ = 0ULL;
            start_ = 0ULL;
            end_ = 0ULL;
            started_ = false;
            ended_ = true;
            for (int i = 0; i < OUTPUTCOUNT; i++)
            {
                outputs_[i].emplace(cfg_.outputs().entry(i), 
                                    service->executor()->active_timers());
            }
            ConfigUpdateService::instance()->register_update_listener(this);
        }
        
        virtual UpdateAction apply_configuration(int fd,
                                                 bool initial_load,
                                                 BarrierNotifiable *done) override
        {
            AutoNotify n(done);
            time_ = cfg_.time().read(fd);
            nextMode_ = (NextMode_t) cfg_.next().read(fd);
            openlcb::EventId cfg_start = cfg_.start().read(fd);
            openlcb::EventId cfg_end = cfg_.end().read(fd);
            if (cfg_start != start_ ||
                cfg_end != end_)
            {
                if (!initial_load) 
                {
                    unregister_handler();
                }
                start_ = cfg_start;
                end_ = cfg_end;
                register_handler();
                return REINIT_NEEDED; // Causes events identify.
            }
            return UPDATED;
        }
        virtual void factory_reset(int fd) override
        {
            CDI_FACTORY_RESET(cfg_.time);
            CDI_FACTORY_RESET(cfg_.next);
        }
        void handle_identify_global(const openlcb::EventRegistryEntry &registry_entry, 
                                    openlcb::EventReport *event, BarrierNotifiable *done) override
        {
            if (event->dst_node && event->dst_node != node_)
            {
                done->notify();
                return;
            }
            SendAllProducersIdentified(event,done);
            done->maybe_done();
        }
        void handle_identify_producer(const openlcb::EventRegistryEntry &registry_entry,
                                      openlcb::EventReport *event, 
                                      BarrierNotifiable *done) override
        {
            SendProducerIdentified(event,done);
            done->maybe_done();
        }
        long long StartStep()
        {
            //LOG(INFO,"[Sequence::Step::StartStep]");
            for (int i=0; i < OUTPUTCOUNT; i++)
            {
                outputs_[i]->StartOutput();
            }
            started_ = true;
            ended_ = false;
            return time_ * 1000000ULL;
        }
        void EndStep()
        {
            //LOG(INFO,"[Sequence::Step::EndStep]");
            //for (int i=0; i < OUTPUTCOUNT; i++)
            //{
            //    outputs_[i]->log_duty();
            //}
            started_ = false;
            ended_ = true;
        }
        void StopFlicker()
        {
            for (int i=0; i < OUTPUTCOUNT; i++)
            {
                outputs_[i]->StopFlicker();
            }
        }
        openlcb::EventId StartEventId() const 
        {
            return start_;
        }
        openlcb::EventId EndEventId() const 
        {
            return end_;
        }
        NextMode_t NextMode() const
        {
            return nextMode_;
        }
    private:
        void register_handler()
        {
            openlcb::EventRegistry::instance()->register_handler(
                                                                 openlcb::EventRegistryEntry(this, start_), 0);
            openlcb::EventRegistry::instance()->register_handler(
                                                                 openlcb::EventRegistryEntry(this, end_), 0);
        }
        void unregister_handler()
        {
            openlcb::EventRegistry::instance()->unregister_handler(this);
        }
        void SendAllProducersIdentified(openlcb::EventReport *event,BarrierNotifiable *done)
        {
            openlcb::Defs::MTI mti_started = openlcb::Defs::MTI_PRODUCER_IDENTIFIED_INVALID,
                  mti_ended = openlcb::Defs::MTI_PRODUCER_IDENTIFIED_INVALID;
            if (started_) 
            {
                mti_started = openlcb::Defs::MTI_PRODUCER_IDENTIFIED_VALID;
            }
            if (ended_)
            {
                mti_ended = openlcb::Defs::MTI_PRODUCER_IDENTIFIED_VALID;
            }
            event->event_write_helper<1>()->WriteAsync(node_,
                                                       mti_started,
                                                       openlcb::WriteHelper::global(),
                                                       openlcb::eventid_to_buffer(start_),
                                                       done->new_child());
            event->event_write_helper<2>()->WriteAsync(node_,
                                                       mti_ended,
                                                       openlcb::WriteHelper::global(),
                                                       openlcb::eventid_to_buffer(end_),
                                                       done->new_child());
        }
        void SendProducerIdentified(openlcb::EventReport *event,BarrierNotifiable *done)
        {
            openlcb::Defs::MTI mti = openlcb::Defs::MTI_PRODUCER_IDENTIFIED_UNKNOWN;
            if (event->event == start_)
            {
                if (started_) mti = openlcb::Defs::MTI_PRODUCER_IDENTIFIED_VALID;
                else mti = openlcb::Defs::MTI_PRODUCER_IDENTIFIED_INVALID;
            }
            else if (event->event == end_)
            {
                if (ended_) mti = openlcb::Defs::MTI_PRODUCER_IDENTIFIED_VALID;
                else mti = openlcb::Defs::MTI_PRODUCER_IDENTIFIED_INVALID;
            }
            event->event_write_helper<3>()->WriteAsync(node_, mti,
                                                       openlcb::WriteHelper::global(),
                                                       openlcb::eventid_to_buffer(event->event),
                                                       done->new_child());
        }
        const StepConfig cfg_;
        openlcb::EventId start_;
        openlcb::EventId end_;
        long long time_;
        bool started_;
        bool ended_;
        openlcb::Node *node_;
        uninitialized<Output> outputs_[OUTPUTCOUNT];
        NextMode_t nextMode_;
    };
    
    void SendAllConsumersIdentified(openlcb::EventReport *event,BarrierNotifiable *done)
    {
        openlcb::Defs::MTI startmti = openlcb::Defs::MTI_CONSUMER_IDENTIFIED_INVALID;
        openlcb::Defs::MTI stopmti = openlcb::Defs::MTI_CONSUMER_IDENTIFIED_VALID;
        if (running_) 
        {
            startmti = openlcb::Defs::MTI_CONSUMER_IDENTIFIED_VALID;
            stopmti = openlcb::Defs::MTI_CONSUMER_IDENTIFIED_INVALID;
        }
        event->event_write_helper<1>()->WriteAsync(node_, startmti,
                                                   openlcb::WriteHelper::global(),
                                                   openlcb::eventid_to_buffer(start_),
                                                   done->new_child());
        
        event->event_write_helper<2>()->WriteAsync(node_, stopmti,
                                                   openlcb::WriteHelper::global(),
                                                   openlcb::eventid_to_buffer(stop_),
                                                   done->new_child());
        
    }
    void SendConsumerIdentified(openlcb::EventReport *event,BarrierNotifiable *done)
    {
        openlcb::Defs::MTI mti = openlcb::Defs::MTI_CONSUMER_IDENTIFIED_UNKNOWN;
        if (event->event == start_)
        {
            if (running_) 
                mti = openlcb::Defs::MTI_CONSUMER_IDENTIFIED_VALID;
            else
                mti = openlcb::Defs::MTI_CONSUMER_IDENTIFIED_INVALID;
            event->event_write_helper<3>()->WriteAsync(node_, mti, 
                                                       openlcb::WriteHelper::global(),
                                                       openlcb::eventid_to_buffer(event->event),
                                                       done->new_child());
        }
        if (event->event == stop_)
        {
            if (!running_)
                mti = openlcb::Defs::MTI_CONSUMER_IDENTIFIED_VALID;
            else
                mti = openlcb::Defs::MTI_CONSUMER_IDENTIFIED_INVALID;
            event->event_write_helper<4>()->WriteAsync(node_, mti,
                                                       openlcb::WriteHelper::global(),
                                                       openlcb::eventid_to_buffer(event->event),
                                                       done->new_child());
        }
    }
    void unregister_handler()
    {
        openlcb::EventRegistry::instance()->unregister_handler(this);
    }
    void register_handler()
    {
        openlcb::EventRegistry::instance()->register_handler(
           openlcb::EventRegistryEntry(this, start_), 0);
        openlcb::EventRegistry::instance()->register_handler(
           openlcb::EventRegistryEntry(this, stop_), 0);
    }
    StateFlowTimer timer_;
    BarrierNotifiable bn_;
    openlcb::WriteHelper write_helpers[2];
    openlcb::EventId start_;
    openlcb::EventId stop_;
    const SequenceConfig cfg_;
    openlcb::Node *node_;
    uninitialized<Step> steps_[STEPSCOUNT];
    bool stepRunning_;
    bool stopped_;
    bool running_;
    bool enabled_;
    uint8_t istate_;
};
        
        
    
#endif // __SEQUENCE_HXX

