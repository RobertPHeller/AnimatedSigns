// -!- c++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Fri Jul 28 14:52:28 2023
//  Last Modified : <230830.1130>
//
//  Description	
//
//  Notes
//
//  History
//	
/////////////////////////////////////////////////////////////////////////////
/// @copyright
///    Copyright (C) 2023  Robert Heller D/B/A Deepwoods Software
///			51 Locke Hill Road
///			Wendell, MA 01379-9728
///
///    This program is free software; you can redistribute it and/or modify
///    it under the terms of the GNU General Public License as published by
///    the Free Software Foundation; either version 2 of the License, or
///    (at your option) any later version.
///
///    This program is distributed in the hope that it will be useful,
///    but WITHOUT ANY WARRANTY; without even the implied warranty of
///    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
///    GNU General Public License for more details.
///
///    You should have received a copy of the GNU General Public License
///    along with this program; if not, write to the Free Software
///    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
/// @file Hardware.hxx
/// @author Robert Heller
/// @date Fri Jul 28 14:52:28 2023
/// 
///
//////////////////////////////////////////////////////////////////////////////

#ifndef __HARDWARE_HXX
#define __HARDWARE_HXX
#include "Stm32Gpio.hxx"
#include "utils/GpioInitializer.hxx"
#include "BlinkerGPIO.hxx"
#include "DummyGPIO.hxx"
#include "PWM.hxx"

GPIO_PIN(LED_GREEN_RAW, LedPin, A, 5);

// Driver (PWM) pins                     
GPIO_PIN(D10, GpioOutputSafeHigh, D, 14); // TIMER_B_PWM3 - TIM4_CH3 #1 CN7  16
GPIO_PIN(D9, GpioOutputSafeHigh, D, 15);  // TIMER_B_PWM2 - TIM4_CH4 #2 CN7  18
GPIO_PIN(D6, GpioOutputSafeHigh, E, 9);   // TIMER_A_PWM1 - TIM1_CH1 #3 CN10  4
GPIO_PIN(D5, GpioOutputSafeHigh, E, 11);  // TIMER_A_PWM2 - TIM1_CH2 #4 CN10  6
GPIO_PIN(D3, GpioOutputSafeHigh, E, 13);  // TIMER_A_PWM3 - TIM1_CH3 #3 CN10 10
GPIO_PIN(D38, GpioOutputSafeHigh, E, 14); // TIMER_A_PWM4 - TIM1_CH4 #6 CN10 28
GPIO_PIN(D36, GpioOutputSafeHigh, B, 10); // TIMER_C_PWM2 - TIM2_CH3 #7 CN10 32
GPIO_PIN(D35, GpioOutputSafeHigh, B, 11); // TIMER_C_PWM3 - TIM2_CH4 #8 CN10 34

         
typedef GpioInitializer<LED_GREEN_RAW_Pin, //
    D6_Pin, D5_Pin, D3_Pin, D9_Pin, D10_Pin, D38_Pin, 
    D36_Pin, D35_Pin,
    DummyPin>
    GpioInit;

typedef LED_GREEN_RAW_Pin BLINKER_RAW_Pin;
typedef BLINKER_Pin LED_GREEN_Pin;


#include "HardwareDEFS.hxx"


#endif // __HARDWARE_HXX

