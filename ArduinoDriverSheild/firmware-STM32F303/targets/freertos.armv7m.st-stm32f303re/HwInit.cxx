/** \copyright
 * Copyright (c) 2018, Balazs Racz
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are  permitted provided that the following conditions are met:
 *
 *  - Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 *  - Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 * \file HwInit.cxx
 *
 * This file represents the hardware initialization for the STM32F303RE Nucelo
 * board with the DevKit IO board plugged in.
 *
 * @author Balazs Racz
 * @date April 18, 2018
 */

#define _DEFAULT_SOURCE

#include <new>
#include <cstdint>

#include "stm32f3xx_hal_conf.h"
#include "stm32f3xx_hal.h"

#include "os/OS.hxx"
#include "Stm32Uart.hxx"
#include "Stm32Can.hxx"
#include "Stm32SPI.hxx"
#include "Stm32I2C.hxx"
#include "Stm32EEPROMEmulation.hxx"
#include "Stm32PWM.hxx"
#include "Hardware.hxx"

/** override stdin */
const char *STDIN_DEVICE = "/dev/ser0";

/** override stdout */
const char *STDOUT_DEVICE = "/dev/ser0";

/** override stderr */
const char *STDERR_DEVICE = "/dev/ser0";

/** UART 0 serial driver instance */
static Stm32Uart uart0("/dev/ser0", USART2, USART2_IRQn);

/** CAN 0 CAN driver instance */
static Stm32Can can0("/dev/can0");

/** EEPROM emulation driver. The file size might be made bigger. */
static Stm32EEPROMEmulation eeprom0("/dev/eeprom", 8192);
// originally 4000

/** How many bytes of flash should hold the entire dataset. Must be an integer
 * multiple of the minimum erase length (which is the flash page length, for
 * the STM32F0 | STM32F3 it is 2 kbytes). The file size maximum is half this
 * value. */
const size_t EEPROMEmulation::SECTOR_SIZE = 16384;

Stm32PWMGroup pwmtimer_2(TIM2, (configCPU_CLOCK_HZ * 6 / 1000 + 65535) / 65536,
                          configCPU_CLOCK_HZ * 6 / 1000);

Stm32PWMGroup pwmtimer_3(TIM3, (configCPU_CLOCK_HZ * 6 / 1000 + 65535) / 65536,
                          configCPU_CLOCK_HZ * 6 / 1000);

Stm32PWMGroup pwmtimer_4(TIM4, (configCPU_CLOCK_HZ * 6 / 1000 + 65535) / 65536,
                          configCPU_CLOCK_HZ * 6 / 1000);

Stm32PWMGroup pwmtimer_17(TIM17, (configCPU_CLOCK_HZ * 6 / 1000 + 65535) / 65536,
                          configCPU_CLOCK_HZ * 6 / 1000);
Stm32PWMGroup pwmtimer_16(TIM16, (configCPU_CLOCK_HZ * 6 / 1000 + 65535) / 65536,
                          configCPU_CLOCK_HZ * 6 / 1000);

extern PWM* const pwmchannels[];
/// The order of these channels follows the schematic arrangement of MCU pins
/// to logical servo ports.
PWM * const pwmchannels[8] = { //
    Stm32PWMGroup::get_channel(&pwmtimer_2, 4), // D2
    Stm32PWMGroup::get_channel(&pwmtimer_2, 2), // D3
    Stm32PWMGroup::get_channel(&pwmtimer_3, 2), // D4
    Stm32PWMGroup::get_channel(&pwmtimer_3, 1), // D5
    Stm32PWMGroup::get_channel(&pwmtimer_2, 3), // D6
    Stm32PWMGroup::get_channel(&pwmtimer_4, 1), // D10
    Stm32PWMGroup::get_channel(&pwmtimer_17,1), // D11
    Stm32PWMGroup::get_channel(&pwmtimer_16,1) // D12
};

extern "C" {

/** Blink LED */
uint32_t blinker_pattern = 0;
static uint32_t rest_pattern = 0;

void hw_set_to_safe(void)
{
}

void reboot()
{
    NVIC_SystemReset();
}

void resetblink(uint32_t pattern)
{
    blinker_pattern = pattern;
    rest_pattern = pattern ? 1 : 0;
    BLINKER_RAW_Pin::set(pattern ? true : false);
    /* make a timer event trigger immediately */
}

void setblink(uint32_t pattern)
{
    resetblink(pattern);
}

void tim7_trg_com_interrupt_handler(void)
{
    //
    // Clear the timer interrupt.
    //
    TIM7->SR = ~TIM_IT_UPDATE;

    // Set output LED.
    BLINKER_RAW_Pin::set(rest_pattern & 1);

    // Shift and maybe reset pattern.
    rest_pattern >>= 1;
    if (!rest_pattern)
    {
        rest_pattern = blinker_pattern;
    }
}

void diewith(uint32_t pattern)
{
    // vPortClearInterruptMask(0x20);
    asm("cpsie i\n");

    resetblink(pattern);
    while (1)
        ;
}

/** CPU clock speed. */
const unsigned long cm3_cpu_clock_hz = 72000000;
uint32_t SystemCoreClock;
const uint8_t AHBPrescTable[16] = {0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 6, 7, 8, 9};
const uint8_t APBPrescTable[8]  = {0, 0, 0, 0, 1, 2, 3, 4};

/**
  * @brief  System Clock Configuration
  *         The system Clock is configured as follow : 
  *            System Clock source            = PLL (HSE)
  *            SYSCLK(Hz)                     = 72000000
  *            HCLK(Hz)                       = 72000000
  *            AHB Prescaler                  = 1
  *            APB1 Prescaler                 = 2
  *            APB2 Prescaler                 = 1
  *            HSE Frequency(Hz)              = 8000000
  *            HSE PREDIV                     = 1
  *            PLLMUL                         = 9
  *            Flash Latency(WS)              = 2
  * @param  None
  * @retval None
  */
static void clock_setup(void)
{
    HAL_RCC_DeInit();
    
    RCC_ClkInitTypeDef RCC_ClkInitStruct;
    RCC_OscInitTypeDef RCC_OscInitStruct;

    /* Enable HSE Oscillator and activate PLL with HSE as source on bypass
     * mode. This allows using the MCO clock output from the ST_Link part of
     * the nucleo board and freeing up the other clock pin for GPIO. */
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
    RCC_OscInitStruct.HSEState = RCC_HSE_BYPASS;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
    RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
    RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
    RCC_OscInitStruct.PLL.PREDIV = RCC_PREDIV_DIV1;

    HAL_RCC_OscConfig(&RCC_OscInitStruct); 
    	
    /* Select PLL as system clock source and configure the HCLK, PCLK1 and
     * PCLK2 clocks dividers
     */
    RCC_ClkInitStruct.ClockType = (RCC_CLOCKTYPE_SYSCLK | RCC_CLOCKTYPE_HCLK |
                                   RCC_CLOCKTYPE_PCLK1  | RCC_CLOCKTYPE_PCLK2);
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;  
    RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

    HASSERT(HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) == HAL_OK);

    // This will fail if the clocks are somehow misconfigured.
    HASSERT(SystemCoreClock == cm3_cpu_clock_hz);
}

/** Initialize the processor hardware.
 */
void hw_preinit(void)
{
    /* Globally disables interrupts until the FreeRTOS scheduler is up. */
    asm("cpsid i\n");

    /* these FLASH settings enable opertion at 72 MHz */
    __HAL_FLASH_PREFETCH_BUFFER_ENABLE();
    __HAL_FLASH_SET_LATENCY(FLASH_LATENCY_2);

    /* setup the system clock */
    clock_setup();

    /* enable peripheral clocks */
    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();
    __HAL_RCC_GPIOC_CLK_ENABLE();
    __HAL_RCC_GPIOD_CLK_ENABLE();
    __HAL_RCC_GPIOF_CLK_ENABLE();
    __HAL_RCC_USART2_CLK_ENABLE();
    __HAL_RCC_CAN1_CLK_ENABLE();
    __HAL_RCC_TIM7_CLK_ENABLE();
    __HAL_RCC_TIM2_CLK_ENABLE();
    __HAL_RCC_TIM3_CLK_ENABLE();
    __HAL_RCC_TIM4_CLK_ENABLE();
    __HAL_RCC_TIM16_CLK_ENABLE();
    __HAL_RCC_TIM17_CLK_ENABLE();

    /* setup pinmux */
    GPIO_InitTypeDef gpio_init;
    memset(&gpio_init, 0, sizeof(gpio_init));

    /* USART2 pinmux on PA2 and PA3 */
    gpio_init.Mode = GPIO_MODE_AF_PP;
    gpio_init.Pull = GPIO_PULLUP;
    gpio_init.Speed = GPIO_SPEED_FREQ_HIGH;
    gpio_init.Alternate = GPIO_AF7_USART2;
    gpio_init.Pin = GPIO_PIN_2;
    HAL_GPIO_Init(GPIOA, &gpio_init);
    gpio_init.Pin = GPIO_PIN_3;
    HAL_GPIO_Init(GPIOA, &gpio_init);

    /* CAN pinmux on PB8 and PB9 */
    gpio_init.Mode = GPIO_MODE_AF_PP;
    // Disables pull-ups because this is a 5V tolerant pin.
    gpio_init.Pull = GPIO_NOPULL;
    gpio_init.Speed = GPIO_SPEED_FREQ_HIGH;
    gpio_init.Alternate = GPIO_AF9_CAN;
    gpio_init.Pin = GPIO_PIN_8;
    HAL_GPIO_Init(GPIOB, &gpio_init);
    gpio_init.Pin = GPIO_PIN_9;
    HAL_GPIO_Init(GPIOB, &gpio_init);

    GpioInit::hw_init();

    // Switches over PWM timer pins to timer mode.
    // PA10 (AF10_TIM2), PB3 (AF1_TIM2), PB5 (AF2_TIM3), PB4 (AF2_TIM3), 
    // PB10 (AF1_TIM2), PB6 (AF2_TIM4), PA7 (AF1_TIM17), PA6 (AF1_TIM16)
    gpio_init.Mode = GPIO_MODE_AF_PP;
    gpio_init.Pull = GPIO_NOPULL;
    gpio_init.Speed = GPIO_SPEED_FREQ_HIGH;
    gpio_init.Alternate = GPIO_AF10_TIM2;
    gpio_init.Pin = GPIO_PIN_10;
    HAL_GPIO_Init(GPIOA, &gpio_init);
    gpio_init.Alternate = GPIO_AF1_TIM2;
    gpio_init.Pin = GPIO_PIN_3;
    HAL_GPIO_Init(GPIOB, &gpio_init);
    gpio_init.Alternate = GPIO_AF2_TIM3;
    gpio_init.Pin = GPIO_PIN_5;
    HAL_GPIO_Init(GPIOB, &gpio_init);
    gpio_init.Alternate = GPIO_AF2_TIM3;
    gpio_init.Pin = GPIO_PIN_4;
    HAL_GPIO_Init(GPIOB, &gpio_init);
    gpio_init.Alternate = GPIO_AF1_TIM2;
    gpio_init.Pin = GPIO_PIN_10;
    HAL_GPIO_Init(GPIOB, &gpio_init);
    gpio_init.Alternate = GPIO_AF2_TIM4;
    gpio_init.Pin = GPIO_PIN_6;
    HAL_GPIO_Init(GPIOB, &gpio_init);
    gpio_init.Alternate = GPIO_AF1_TIM17;
    gpio_init.Pin = GPIO_PIN_7;
    HAL_GPIO_Init(GPIOA, &gpio_init);
    gpio_init.Alternate = GPIO_AF1_TIM16;
    gpio_init.Pin = GPIO_PIN_6;
    HAL_GPIO_Init(GPIOA, &gpio_init);
    
    /* Initializes the blinker timer. */
    TIM_HandleTypeDef TimHandle;
    memset(&TimHandle, 0, sizeof(TimHandle));
    TimHandle.Instance = TIM7;
    TimHandle.Init.Period = configCPU_CLOCK_HZ / 10000 / 8;
    TimHandle.Init.Prescaler = 10000;
    TimHandle.Init.ClockDivision = 0;
    TimHandle.Init.CounterMode = TIM_COUNTERMODE_UP;
    TimHandle.Init.RepetitionCounter = 0;
    if (HAL_TIM_Base_Init(&TimHandle) != HAL_OK)
    {
        /* Initialization Error */
        HASSERT(0);
    }
    if (HAL_TIM_Base_Start_IT(&TimHandle) != HAL_OK)
    {
        /* Starting Error */
        HASSERT(0);
    }
    __HAL_DBGMCU_FREEZE_TIM7();
    SetInterruptPriority(TIM7_IRQn, 0);
    NVIC_EnableIRQ(TIM7_IRQn);
}

void usart2_interrupt_handler(void)
{
    Stm32Uart::interrupt_handler(1);
}

}
