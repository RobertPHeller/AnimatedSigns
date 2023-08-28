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
//  Last Modified : <230828.1408>
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
GPIO_PIN(D2, GpioOutputSafeHigh, A, 10); // TIM1_CH3  (AF1)  #1 
GPIO_PIN(D3, GpioOutputSafeHigh, B, 3);  // TIM2_CH2  (AF1)  #2
GPIO_PIN(D4, GpioOutputSafeHigh, B, 5);  // TIM3_CH2  (Af2)  #3
GPIO_PIN(D5, GpioOutputSafeHigh, B, 4);  // TIM3_CH1  (Af2)  #4
GPIO_PIN(D6, GpioOutputSafeHigh, B, 10); // TIM2_CH3  (AF1)  #5
GPIO_PIN(D10, GpioOutputSafeHigh, B, 6); // TIM16_CH1 (AF14) #6
GPIO_PIN(D11, GpioOutputSafeHigh, A, 7); // TIM3_CH2  (AF2)  #7
GPIO_PIN(D12, GpioOutputSafeHigh, A, 6); // TIM3_CH1  (AF2)  #8

typedef BLINKER_Pin LED_GREEN_Pin;                

         
typedef GpioInitializer<LED_GREEN_RAW_Pin, //
    D2_Pin, D3_Pin, D4_Pin, D5_Pin, D6_Pin, D10_Pin, 
    D11_Pin, D12_Pin,
    DummyPin>
    GpioInit;

typedef LED_GREEN_RAW_Pin BLINKER_RAW_Pin;
typedef BLINKER_Pin LED_GREEN_Pin;


#include "HardwareDEFS.hxx"


#endif // __HARDWARE_HXX

