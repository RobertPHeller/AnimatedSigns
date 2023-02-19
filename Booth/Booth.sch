EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:switches
LIBS:relays
LIBS:motors
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:6footfl-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L R R101
U 1 1 63F2746C
P 3850 2225
F 0 "R101" V 3930 2225 50  0000 C CNN
F 1 "150" V 3850 2225 50  0000 C CNN
F 2 "Resistors_SMD:R_0402" V 3780 2225 50  0001 C CNN
F 3 "" H 3850 2225 50  0001 C CNN
F 4 "603-RC0402JR-13150RL" V 3850 2225 60  0001 C CNN "Mouser Part Number"
	1    3850 2225
	0    1    1    0   
$EndComp
$Comp
L LED D101
U 1 1 63F2746D
P 3400 2225
F 0 "D101" H 3400 2325 50  0000 C CNN
F 1 "LIGHT" H 3400 2125 50  0000 C CNN
F 2 "LEDs:LED_0402" H 3400 2225 50  0001 C CNN
F 3 "" H 3400 2225 50  0001 C CNN
F 4 "743-IN-S42ATUW" H 3400 2225 60  0001 C CNN "Mouser Part Number"
	1    3400 2225
	1    0    0    -1  
$EndComp
$Comp
L LED D102
U 1 1 63F2746E
P 4275 2225
F 0 "D102" H 4275 2325 50  0000 C CNN
F 1 "LIGHT" H 4275 2125 50  0000 C CNN
F 2 "LEDs:LED_0402" H 4275 2225 50  0001 C CNN
F 3 "" H 4275 2225 50  0001 C CNN
F 4 "743-IN-S42ATUW" H 4275 2225 60  0001 C CNN "Mouser Part Number"
	1    4275 2225
	1    0    0    -1  
$EndComp
$Comp
L LED D103
U 1 1 63F2746F
P 4750 2225
F 0 "D103" H 4750 2325 50  0000 C CNN
F 1 "LIGHT" H 4750 2125 50  0000 C CNN
F 2 "LEDs:LED_0402" H 4750 2225 50  0001 C CNN
F 3 "" H 4750 2225 50  0001 C CNN
F 4 "743-IN-S42ATUW" H 4750 2225 60  0001 C CNN "Mouser Part Number"
	1    4750 2225
	1    0    0    -1  
$EndComp
$Comp
L Conn_01x01 J102
U 1 1 63F27470
P 5150 2225
F 0 "J102" H 5150 2325 50  0000 C CNN
F 1 "+" H 5150 2125 50  0000 C CNN
F 2 "BackPads:BottomPad" H 5150 2225 50  0001 C CNN
F 3 "" H 5150 2225 50  0001 C CNN
	1    5150 2225
	1    0    0    -1  
$EndComp
$Comp
L Conn_01x01 J101
U 1 1 63F27471
P 2975 2225
F 0 "J101" H 2975 2325 50  0000 C CNN
F 1 "-" H 2975 2125 50  0000 C CNN
F 2 "BackPads:BottomPad" H 2975 2225 50  0001 C CNN
F 3 "" H 2975 2225 50  0001 C CNN
	1    2975 2225
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3175 2225 3250 2225
Wire Wire Line
	3550 2225 3700 2225
Wire Wire Line
	4000 2225 4125 2225
Wire Wire Line
	4425 2225 4600 2225
Wire Wire Line
	4900 2225 4950 2225
Text Label 4925 2225 1    60   ~ 0
Plus
Text Label 3200 2225 3    60   ~ 0
Minus
$EndSCHEMATC
