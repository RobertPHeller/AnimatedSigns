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
LIBS:tbd62x83a
LIBS:led_3in1
LIBS:8BallLEDPCB-cache
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
L Conn_01x07 J101
U 1 1 63DE8B33
P 8150 1525
F 0 "J101" H 8150 1925 50  0000 C CNN
F 1 "Solder pads" H 8150 1125 50  0000 C CNN
F 2 "SolderPads:PowerPlus5" H 8150 1525 50  0001 C CNN
F 3 "" H 8150 1525 50  0001 C CNN
	1    8150 1525
	1    0    0    -1  
$EndComp
$Comp
L +VDC #PWR02
U 1 1 63DE8BD5
P 7850 1225
F 0 "#PWR02" H 7850 1125 50  0001 C CNN
F 1 "+VDC" H 7850 1475 50  0000 C CNN
F 2 "" H 7850 1225 50  0001 C CNN
F 3 "" H 7850 1225 50  0001 C CNN
	1    7850 1225
	0    -1   -1   0   
$EndComp
$Comp
L Conn_01x07 J102
U 1 1 63DE8C4C
P 8900 1525
F 0 "J102" H 8900 1925 50  0000 C CNN
F 1 "Solder pads" H 8900 1125 50  0000 C CNN
F 2 "SolderPads:PowerPlus5" H 8900 1525 50  0001 C CNN
F 3 "" H 8900 1525 50  0001 C CNN
	1    8900 1525
	-1   0    0    -1  
$EndComp
$Comp
L +VDC #PWR04
U 1 1 63DE8C59
P 9200 1225
F 0 "#PWR04" H 9200 1125 50  0001 C CNN
F 1 "+VDC" H 9200 1475 50  0000 C CNN
F 2 "" H 9200 1225 50  0001 C CNN
F 3 "" H 9200 1225 50  0001 C CNN
	1    9200 1225
	0    1    -1   0   
$EndComp
Text Label 7950 1325 2    60   ~ 0
AL
Text Label 9100 1325 0    60   ~ 0
AR
Text Label 7950 1425 2    60   ~ 0
BL
Text Label 7950 1525 2    60   ~ 0
CL
Text Label 7950 1625 2    60   ~ 0
DL
Text Label 7950 1725 2    60   ~ 0
EL
Text Label 9100 1425 0    60   ~ 0
BR
Text Label 9100 1525 0    60   ~ 0
CR
Text Label 9100 1625 0    60   ~ 0
DR
Text Label 9100 1725 0    60   ~ 0
ER
Text Label 7050 2650 2    60   ~ 0
AL
Text Label 7275 3250 2    60   ~ 0
BL
Text Label 7450 3950 2    60   ~ 0
CL
Text Label 7575 4500 2    60   ~ 0
DL
Text Label 7625 5325 2    60   ~ 0
EL
Text Label 3450 2125 2    60   ~ 0
AR
Text Label 3600 2775 2    60   ~ 0
BR
Text Label 3825 3600 2    60   ~ 0
CR
Text Label 3875 4175 2    60   ~ 0
DR
Text Label 3725 4875 2    60   ~ 0
ER
$Comp
L R R108
U 1 1 63DEAC30
P 4375 4175
F 0 "R108" V 4455 4175 50  0000 C CNN
F 1 "150" V 4375 4175 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 4305 4175 50  0001 C CNN
F 3 "" H 4375 4175 50  0001 C CNN
F 4 "603-RT0603FRE13150RL" V 4375 4175 60  0001 C CNN "Mouser Part Number"
	1    4375 4175
	0    1    1    0   
$EndComp
Wire Wire Line
	7950 1825 7850 1825
Wire Wire Line
	7850 1225 7950 1225
Wire Wire Line
	9100 1825 9200 1825
Wire Wire Line
	9200 1225 9100 1225
Wire Wire Line
	7575 4500 7650 4500
Wire Wire Line
	3875 4175 4225 4175
$Comp
L LED D103
U 1 1 63DEEF89
P 4850 4175
F 0 "D103" H 4850 4275 50  0000 C CNN
F 1 "BALL" H 4850 4075 50  0000 C CNN
F 2 "LEDs:LED_1206" H 4850 4175 50  0001 C CNN
F 3 "" H 4850 4175 50  0001 C CNN
F 4 "743-S126AT5UW" H 4850 4175 60  0001 C CNN "Mouser Part Number"
	1    4850 4175
	1    0    0    -1  
$EndComp
$Comp
L LED D104
U 1 1 63DEF1A9
P 5300 4175
F 0 "D104" H 5300 4275 50  0000 C CNN
F 1 "BALL" H 5300 4075 50  0000 C CNN
F 2 "LEDs:LED_1206" H 5300 4175 50  0001 C CNN
F 3 "" H 5300 4175 50  0001 C CNN
F 4 "743-S126AT5UW" H 5300 4175 60  0001 C CNN "Mouser Part Number"
	1    5300 4175
	1    0    0    -1  
$EndComp
$Comp
L LED D105
U 1 1 63DEF26B
P 5700 4175
F 0 "D105" H 5700 4275 50  0000 C CNN
F 1 "BALL" H 5700 4075 50  0000 C CNN
F 2 "LEDs:LED_1206" H 5700 4175 50  0001 C CNN
F 3 "" H 5700 4175 50  0001 C CNN
F 4 "743-S126AT5UW" H 5700 4175 60  0001 C CNN "Mouser Part Number"
	1    5700 4175
	1    0    0    -1  
$EndComp
Wire Wire Line
	4525 4175 4700 4175
Wire Wire Line
	5000 4175 5150 4175
Wire Wire Line
	5450 4175 5550 4175
$Comp
L +VDC #PWR05
U 1 1 63DEF385
P 5950 4175
F 0 "#PWR05" H 5950 4075 50  0001 C CNN
F 1 "+VDC" H 5950 4425 50  0000 C CNN
F 2 "" H 5950 4175 50  0001 C CNN
F 3 "" H 5950 4175 50  0001 C CNN
	1    5950 4175
	0    1    1    0   
$EndComp
Wire Wire Line
	5850 4175 5950 4175
$Comp
L R R101
U 1 1 63DEFC1D
P 7800 4500
F 0 "R101" V 7880 4500 50  0000 C CNN
F 1 "150" V 7800 4500 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 7730 4500 50  0001 C CNN
F 3 "" H 7800 4500 50  0001 C CNN
F 4 "603-RT0603FRE13150RL" V 7800 4500 60  0001 C CNN "Mouser Part Number"
	1    7800 4500
	0    1    1    0   
$EndComp
$Comp
L LED D106
U 1 1 63DEFC25
P 8250 4500
F 0 "D106" H 8250 4600 50  0000 C CNN
F 1 "BALL" H 8250 4400 50  0000 C CNN
F 2 "LEDs:LED_1206" H 8250 4500 50  0001 C CNN
F 3 "" H 8250 4500 50  0001 C CNN
F 4 "743-S126AT5UW" H 8250 4500 60  0001 C CNN "Mouser Part Number"
	1    8250 4500
	1    0    0    -1  
$EndComp
$Comp
L LED D107
U 1 1 63DEFC2C
P 8700 4500
F 0 "D107" H 8700 4600 50  0000 C CNN
F 1 "BALL" H 8700 4400 50  0000 C CNN
F 2 "LEDs:LED_1206" H 8700 4500 50  0001 C CNN
F 3 "" H 8700 4500 50  0001 C CNN
F 4 "743-S126AT5UW" H 8700 4500 60  0001 C CNN "Mouser Part Number"
	1    8700 4500
	1    0    0    -1  
$EndComp
$Comp
L LED D108
U 1 1 63DEFC33
P 9150 4500
F 0 "D108" H 9150 4600 50  0000 C CNN
F 1 "BALL" H 9150 4400 50  0000 C CNN
F 2 "LEDs:LED_1206" H 9150 4500 50  0001 C CNN
F 3 "" H 9150 4500 50  0001 C CNN
F 4 "743-S126AT5UW" H 9150 4500 60  0001 C CNN "Mouser Part Number"
	1    9150 4500
	1    0    0    -1  
$EndComp
Wire Wire Line
	7950 4500 8100 4500
Wire Wire Line
	8400 4500 8550 4500
Wire Wire Line
	8850 4500 9000 4500
$Comp
L +VDC #PWR06
U 1 1 63DEFC3C
P 9400 4500
F 0 "#PWR06" H 9400 4400 50  0001 C CNN
F 1 "+VDC" H 9400 4750 50  0000 C CNN
F 2 "" H 9400 4500 50  0001 C CNN
F 3 "" H 9400 4500 50  0001 C CNN
	1    9400 4500
	0    1    1    0   
$EndComp
Wire Wire Line
	9300 4500 9400 4500
Wire Wire Line
	7625 5325 7700 5325
$Comp
L R R110
U 1 1 63DF4CE6
P 7850 5325
F 0 "R110" V 7930 5325 50  0000 C CNN
F 1 "150" V 7850 5325 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 7780 5325 50  0001 C CNN
F 3 "" H 7850 5325 50  0001 C CNN
F 4 "603-RT0603FRE13150RL" V 7850 5325 60  0001 C CNN "Mouser Part Number"
	1    7850 5325
	0    1    1    0   
$EndComp
$Comp
L LED D123
U 1 1 63DF4CED
P 8300 5325
F 0 "D123" H 8300 5425 50  0000 C CNN
F 1 "8BALL" H 8300 5225 50  0000 C CNN
F 2 "LEDs:LED_1206" H 8300 5325 50  0001 C CNN
F 3 "" H 8300 5325 50  0001 C CNN
F 4 "743-S126AT5UW" H 8300 5325 60  0001 C CNN "Mouser Part Number"
	1    8300 5325
	1    0    0    -1  
$EndComp
$Comp
L LED D127
U 1 1 63DF4CF4
P 8750 5325
F 0 "D127" H 8750 5425 50  0000 C CNN
F 1 "8BALL" H 8750 5225 50  0000 C CNN
F 2 "LEDs:LED_1206" H 8750 5325 50  0001 C CNN
F 3 "" H 8750 5325 50  0001 C CNN
F 4 "743-S126AT5UW" H 8750 5325 60  0001 C CNN "Mouser Part Number"
	1    8750 5325
	1    0    0    -1  
$EndComp
$Comp
L LED D130
U 1 1 63DF4CFB
P 9200 5325
F 0 "D130" H 9200 5425 50  0000 C CNN
F 1 "8BALL" H 9200 5225 50  0000 C CNN
F 2 "LEDs:LED_1206" H 9200 5325 50  0001 C CNN
F 3 "" H 9200 5325 50  0001 C CNN
F 4 "743-S126AT5UW" H 9200 5325 60  0001 C CNN "Mouser Part Number"
	1    9200 5325
	1    0    0    -1  
$EndComp
Wire Wire Line
	8000 5325 8150 5325
Wire Wire Line
	8450 5325 8600 5325
Wire Wire Line
	8900 5325 9050 5325
$Comp
L +VDC #PWR07
U 1 1 63DF4D04
P 9450 5325
F 0 "#PWR07" H 9450 5225 50  0001 C CNN
F 1 "+VDC" H 9450 5575 50  0000 C CNN
F 2 "" H 9450 5325 50  0001 C CNN
F 3 "" H 9450 5325 50  0001 C CNN
	1    9450 5325
	0    1    1    0   
$EndComp
Wire Wire Line
	9350 5325 9450 5325
$Comp
L R R105
U 1 1 63DF5038
P 4225 4875
F 0 "R105" V 4305 4875 50  0000 C CNN
F 1 "150" V 4225 4875 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 4155 4875 50  0001 C CNN
F 3 "" H 4225 4875 50  0001 C CNN
F 4 "603-RT0603FRE13150RL" V 4225 4875 60  0001 C CNN "Mouser Part Number"
	1    4225 4875
	0    1    1    0   
$EndComp
Wire Wire Line
	3725 4875 4075 4875
$Comp
L LED D111
U 1 1 63DF5040
P 4700 4875
F 0 "D111" H 4700 4975 50  0000 C CNN
F 1 "8BALL" H 4700 4775 50  0000 C CNN
F 2 "LEDs:LED_1206" H 4700 4875 50  0001 C CNN
F 3 "" H 4700 4875 50  0001 C CNN
F 4 "743-S126AT5UW" H 4700 4875 60  0001 C CNN "Mouser Part Number"
	1    4700 4875
	1    0    0    -1  
$EndComp
$Comp
L LED D115
U 1 1 63DF5047
P 5150 4875
F 0 "D115" H 5150 4975 50  0000 C CNN
F 1 "8BALL" H 5150 4775 50  0000 C CNN
F 2 "LEDs:LED_1206" H 5150 4875 50  0001 C CNN
F 3 "" H 5150 4875 50  0001 C CNN
F 4 "743-S126AT5UW" H 5150 4875 60  0001 C CNN "Mouser Part Number"
	1    5150 4875
	1    0    0    -1  
$EndComp
$Comp
L LED D118
U 1 1 63DF504E
P 5550 4875
F 0 "D118" H 5550 4975 50  0000 C CNN
F 1 "8BALL" H 5550 4775 50  0000 C CNN
F 2 "LEDs:LED_1206" H 5550 4875 50  0001 C CNN
F 3 "" H 5550 4875 50  0001 C CNN
F 4 "743-S126AT5UW" H 5550 4875 60  0001 C CNN "Mouser Part Number"
	1    5550 4875
	1    0    0    -1  
$EndComp
Wire Wire Line
	4375 4875 4550 4875
Wire Wire Line
	4850 4875 5000 4875
Wire Wire Line
	5300 4875 5400 4875
$Comp
L +VDC #PWR08
U 1 1 63DF5057
P 5800 4875
F 0 "#PWR08" H 5800 4775 50  0001 C CNN
F 1 "+VDC" H 5800 5125 50  0000 C CNN
F 2 "" H 5800 4875 50  0001 C CNN
F 3 "" H 5800 4875 50  0001 C CNN
	1    5800 4875
	0    1    1    0   
$EndComp
Wire Wire Line
	5700 4875 5800 4875
Wire Wire Line
	7450 3950 7525 3950
$Comp
L R R109
U 1 1 63DF58AE
P 7675 3950
F 0 "R109" V 7755 3950 50  0000 C CNN
F 1 "150" V 7675 3950 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 7605 3950 50  0001 C CNN
F 3 "" H 7675 3950 50  0001 C CNN
F 4 "603-RT0603FRE13150RL" V 7675 3950 60  0001 C CNN "Mouser Part Number"
	1    7675 3950
	0    1    1    0   
$EndComp
$Comp
L LED D121
U 1 1 63DF58B5
P 8125 3950
F 0 "D121" H 8125 4050 50  0000 C CNN
F 1 "CLUB" H 8125 3850 50  0000 C CNN
F 2 "LEDs:LED_1206" H 8125 3950 50  0001 C CNN
F 3 "" H 8125 3950 50  0001 C CNN
F 4 "743-S126AT5UW" H 8125 3950 60  0001 C CNN "Mouser Part Number"
	1    8125 3950
	1    0    0    -1  
$EndComp
$Comp
L LED D125
U 1 1 63DF58BC
P 8575 3950
F 0 "D125" H 8575 4050 50  0000 C CNN
F 1 "CLUB" H 8575 3850 50  0000 C CNN
F 2 "LEDs:LED_1206" H 8575 3950 50  0001 C CNN
F 3 "" H 8575 3950 50  0001 C CNN
F 4 "743-S126AT5UW" H 8575 3950 60  0001 C CNN "Mouser Part Number"
	1    8575 3950
	1    0    0    -1  
$EndComp
$Comp
L LED D129
U 1 1 63DF58C3
P 9025 3950
F 0 "D129" H 9025 4050 50  0000 C CNN
F 1 "CLUB" H 9025 3850 50  0000 C CNN
F 2 "LEDs:LED_1206" H 9025 3950 50  0001 C CNN
F 3 "" H 9025 3950 50  0001 C CNN
F 4 "743-S126AT5UW" H 9025 3950 60  0001 C CNN "Mouser Part Number"
	1    9025 3950
	1    0    0    -1  
$EndComp
Wire Wire Line
	7825 3950 7975 3950
Wire Wire Line
	8275 3950 8425 3950
Wire Wire Line
	8725 3950 8875 3950
$Comp
L +VDC #PWR09
U 1 1 63DF58CC
P 9275 3950
F 0 "#PWR09" H 9275 3850 50  0001 C CNN
F 1 "+VDC" H 9275 4200 50  0000 C CNN
F 2 "" H 9275 3950 50  0001 C CNN
F 3 "" H 9275 3950 50  0001 C CNN
	1    9275 3950
	0    1    1    0   
$EndComp
Wire Wire Line
	9175 3950 9275 3950
Wire Wire Line
	3825 3600 3900 3600
$Comp
L R R104
U 1 1 63DF5DF3
P 4050 3600
F 0 "R104" V 4130 3600 50  0000 C CNN
F 1 "150" V 4050 3600 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 3980 3600 50  0001 C CNN
F 3 "" H 4050 3600 50  0001 C CNN
F 4 "603-RT0603FRE13150RL" V 4050 3600 60  0001 C CNN "Mouser Part Number"
	1    4050 3600
	0    1    1    0   
$EndComp
$Comp
L LED D109
U 1 1 63DF5DFA
P 4500 3600
F 0 "D109" H 4500 3700 50  0000 C CNN
F 1 "CLUB" H 4500 3500 50  0000 C CNN
F 2 "LEDs:LED_1206" H 4500 3600 50  0001 C CNN
F 3 "" H 4500 3600 50  0001 C CNN
F 4 "743-S126AT5UW" H 4500 3600 60  0001 C CNN "Mouser Part Number"
	1    4500 3600
	1    0    0    -1  
$EndComp
$Comp
L LED D113
U 1 1 63DF5E01
P 4950 3600
F 0 "D113" H 4950 3700 50  0000 C CNN
F 1 "CLUB" H 4950 3500 50  0000 C CNN
F 2 "LEDs:LED_1206" H 4950 3600 50  0001 C CNN
F 3 "" H 4950 3600 50  0001 C CNN
F 4 "743-S126AT5UW" H 4950 3600 60  0001 C CNN "Mouser Part Number"
	1    4950 3600
	1    0    0    -1  
$EndComp
$Comp
L LED D117
U 1 1 63DF5E08
P 5400 3600
F 0 "D117" H 5400 3700 50  0000 C CNN
F 1 "CLUB" H 5400 3500 50  0000 C CNN
F 2 "LEDs:LED_1206" H 5400 3600 50  0001 C CNN
F 3 "" H 5400 3600 50  0001 C CNN
F 4 "743-S126AT5UW" H 5400 3600 60  0001 C CNN "Mouser Part Number"
	1    5400 3600
	1    0    0    -1  
$EndComp
Wire Wire Line
	4200 3600 4350 3600
Wire Wire Line
	4650 3600 4800 3600
Wire Wire Line
	5100 3600 5250 3600
$Comp
L +VDC #PWR010
U 1 1 63DF5E11
P 5650 3600
F 0 "#PWR010" H 5650 3500 50  0001 C CNN
F 1 "+VDC" H 5650 3850 50  0000 C CNN
F 2 "" H 5650 3600 50  0001 C CNN
F 3 "" H 5650 3600 50  0001 C CNN
	1    5650 3600
	0    1    1    0   
$EndComp
Wire Wire Line
	5550 3600 5650 3600
Wire Wire Line
	3600 2775 3675 2775
$Comp
L R R103
U 1 1 63DF64DA
P 3825 2775
F 0 "R103" V 3905 2775 50  0000 C CNN
F 1 "150" V 3825 2775 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 3755 2775 50  0001 C CNN
F 3 "" H 3825 2775 50  0001 C CNN
F 4 "603-RT0603FRE13150RL" V 3825 2775 60  0001 C CNN "Mouser Part Number"
	1    3825 2775
	0    1    1    0   
$EndComp
$Comp
L LED D102
U 1 1 63DF64E1
P 4275 2775
F 0 "D102" H 4275 2875 50  0000 C CNN
F 1 "CUE" H 4275 2675 50  0000 C CNN
F 2 "LEDs:LED_1206" H 4275 2775 50  0001 C CNN
F 3 "" H 4275 2775 50  0001 C CNN
F 4 "743-S126AT5UW" H 4275 2775 60  0001 C CNN "Mouser Part Number"
	1    4275 2775
	1    0    0    -1  
$EndComp
$Comp
L LED D112
U 1 1 63DF64E8
P 4725 2775
F 0 "D112" H 4725 2875 50  0000 C CNN
F 1 "CUE" H 4725 2675 50  0000 C CNN
F 2 "LEDs:LED_1206" H 4725 2775 50  0001 C CNN
F 3 "" H 4725 2775 50  0001 C CNN
F 4 "743-S126AT5UW" H 4725 2775 60  0001 C CNN "Mouser Part Number"
	1    4725 2775
	1    0    0    -1  
$EndComp
$Comp
L LED D116
U 1 1 63DF64EF
P 5175 2775
F 0 "D116" H 5175 2875 50  0000 C CNN
F 1 "CUE" H 5175 2675 50  0000 C CNN
F 2 "LEDs:LED_1206" H 5175 2775 50  0001 C CNN
F 3 "" H 5175 2775 50  0001 C CNN
F 4 "743-S126AT5UW" H 5175 2775 60  0001 C CNN "Mouser Part Number"
	1    5175 2775
	1    0    0    -1  
$EndComp
Wire Wire Line
	3975 2775 4125 2775
Wire Wire Line
	4425 2775 4575 2775
Wire Wire Line
	4875 2775 5025 2775
$Comp
L +VDC #PWR011
U 1 1 63DF64F8
P 5425 2775
F 0 "#PWR011" H 5425 2675 50  0001 C CNN
F 1 "+VDC" H 5425 3025 50  0000 C CNN
F 2 "" H 5425 2775 50  0001 C CNN
F 3 "" H 5425 2775 50  0001 C CNN
	1    5425 2775
	0    1    1    0   
$EndComp
Wire Wire Line
	5325 2775 5425 2775
Wire Wire Line
	3450 2125 3525 2125
$Comp
L R R102
U 1 1 63DF6751
P 3675 2125
F 0 "R102" V 3755 2125 50  0000 C CNN
F 1 "150" V 3675 2125 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 3605 2125 50  0001 C CNN
F 3 "" H 3675 2125 50  0001 C CNN
F 4 "603-RT0603FRE13150RL" V 3675 2125 60  0001 C CNN "Mouser Part Number"
	1    3675 2125
	0    1    1    0   
$EndComp
$Comp
L LED D101
U 1 1 63DF6758
P 4125 2125
F 0 "D101" H 4125 2225 50  0000 C CNN
F 1 "ARROW" H 4125 2025 50  0000 C CNN
F 2 "LEDs:LED_1206" H 4125 2125 50  0001 C CNN
F 3 "" H 4125 2125 50  0001 C CNN
F 4 "743-S126AT5UW" H 4125 2125 60  0001 C CNN "Mouser Part Number"
	1    4125 2125
	1    0    0    -1  
$EndComp
$Comp
L LED D110
U 1 1 63DF675F
P 4575 2125
F 0 "D110" H 4575 2225 50  0000 C CNN
F 1 "ARROW" H 4575 2025 50  0000 C CNN
F 2 "LEDs:LED_1206" H 4575 2125 50  0001 C CNN
F 3 "" H 4575 2125 50  0001 C CNN
F 4 "743-S126AT5UW" H 4575 2125 60  0001 C CNN "Mouser Part Number"
	1    4575 2125
	1    0    0    -1  
$EndComp
$Comp
L LED D114
U 1 1 63DF6766
P 5025 2125
F 0 "D114" H 5025 2225 50  0000 C CNN
F 1 "ARROW" H 5025 2025 50  0000 C CNN
F 2 "LEDs:LED_1206" H 5025 2125 50  0001 C CNN
F 3 "" H 5025 2125 50  0001 C CNN
F 4 "743-S126AT5UW" H 5025 2125 60  0001 C CNN "Mouser Part Number"
	1    5025 2125
	1    0    0    -1  
$EndComp
Wire Wire Line
	3825 2125 3975 2125
Wire Wire Line
	4275 2125 4425 2125
Wire Wire Line
	4725 2125 4875 2125
$Comp
L +VDC #PWR012
U 1 1 63DF676F
P 5275 2125
F 0 "#PWR012" H 5275 2025 50  0001 C CNN
F 1 "+VDC" H 5275 2375 50  0000 C CNN
F 2 "" H 5275 2125 50  0001 C CNN
F 3 "" H 5275 2125 50  0001 C CNN
	1    5275 2125
	0    1    1    0   
$EndComp
Wire Wire Line
	5175 2125 5275 2125
Wire Wire Line
	7275 3250 7350 3250
$Comp
L R R107
U 1 1 63DF6A0C
P 7500 3250
F 0 "R107" V 7580 3250 50  0000 C CNN
F 1 "150" V 7500 3250 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 7430 3250 50  0001 C CNN
F 3 "" H 7500 3250 50  0001 C CNN
F 4 "603-RT0603FRE13150RL" V 7500 3250 60  0001 C CNN "Mouser Part Number"
	1    7500 3250
	0    1    1    0   
$EndComp
$Comp
L LED D120
U 1 1 63DF6A13
P 7950 3250
F 0 "D120" H 7950 3350 50  0000 C CNN
F 1 "CUE" H 7950 3150 50  0000 C CNN
F 2 "LEDs:LED_1206" H 7950 3250 50  0001 C CNN
F 3 "" H 7950 3250 50  0001 C CNN
F 4 "743-S126AT5UW" H 7950 3250 60  0001 C CNN "Mouser Part Number"
	1    7950 3250
	1    0    0    -1  
$EndComp
$Comp
L LED D124
U 1 1 63DF6A1A
P 8400 3250
F 0 "D124" H 8400 3350 50  0000 C CNN
F 1 "CUE" H 8400 3150 50  0000 C CNN
F 2 "LEDs:LED_1206" H 8400 3250 50  0001 C CNN
F 3 "" H 8400 3250 50  0001 C CNN
F 4 "743-S126AT5UW" H 8400 3250 60  0001 C CNN "Mouser Part Number"
	1    8400 3250
	1    0    0    -1  
$EndComp
$Comp
L LED D128
U 1 1 63DF6A21
P 8850 3250
F 0 "D128" H 8850 3350 50  0000 C CNN
F 1 "CUE" H 8850 3150 50  0000 C CNN
F 2 "LEDs:LED_1206" H 8850 3250 50  0001 C CNN
F 3 "" H 8850 3250 50  0001 C CNN
F 4 "743-S126AT5UW" H 8850 3250 60  0001 C CNN "Mouser Part Number"
	1    8850 3250
	1    0    0    -1  
$EndComp
Wire Wire Line
	7650 3250 7800 3250
Wire Wire Line
	8100 3250 8250 3250
Wire Wire Line
	8550 3250 8700 3250
$Comp
L +VDC #PWR013
U 1 1 63DF6A2A
P 9100 3250
F 0 "#PWR013" H 9100 3150 50  0001 C CNN
F 1 "+VDC" H 9100 3500 50  0000 C CNN
F 2 "" H 9100 3250 50  0001 C CNN
F 3 "" H 9100 3250 50  0001 C CNN
	1    9100 3250
	0    1    1    0   
$EndComp
Wire Wire Line
	9000 3250 9100 3250
Wire Wire Line
	7050 2650 7125 2650
$Comp
L R R106
U 1 1 63DF6C80
P 7275 2650
F 0 "R106" V 7355 2650 50  0000 C CNN
F 1 "150" V 7275 2650 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 7205 2650 50  0001 C CNN
F 3 "" H 7275 2650 50  0001 C CNN
F 4 "603-RT0603FRE13150RL" V 7275 2650 60  0001 C CNN "Mouser Part Number"
	1    7275 2650
	0    1    1    0   
$EndComp
$Comp
L LED D119
U 1 1 63DF6C87
P 7725 2650
F 0 "D119" H 7725 2750 50  0000 C CNN
F 1 "ARROW" H 7725 2550 50  0000 C CNN
F 2 "LEDs:LED_1206" H 7725 2650 50  0001 C CNN
F 3 "" H 7725 2650 50  0001 C CNN
F 4 "743-S126AT5UW" H 7725 2650 60  0001 C CNN "Mouser Part Number"
	1    7725 2650
	1    0    0    -1  
$EndComp
$Comp
L LED D122
U 1 1 63DF6C8E
P 8175 2650
F 0 "D122" H 8175 2750 50  0000 C CNN
F 1 "ARROW" H 8175 2550 50  0000 C CNN
F 2 "LEDs:LED_1206" H 8175 2650 50  0001 C CNN
F 3 "" H 8175 2650 50  0001 C CNN
F 4 "743-S126AT5UW" H 8175 2650 60  0001 C CNN "Mouser Part Number"
	1    8175 2650
	1    0    0    -1  
$EndComp
$Comp
L LED D126
U 1 1 63DF6C95
P 8625 2650
F 0 "D126" H 8625 2750 50  0000 C CNN
F 1 "ARROW" H 8625 2550 50  0000 C CNN
F 2 "LEDs:LED_1206" H 8625 2650 50  0001 C CNN
F 3 "" H 8625 2650 50  0001 C CNN
F 4 "743-S126AT5UW" H 8625 2650 60  0001 C CNN "Mouser Part Number"
	1    8625 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	7425 2650 7575 2650
Wire Wire Line
	7875 2650 8025 2650
Wire Wire Line
	8325 2650 8475 2650
$Comp
L +VDC #PWR014
U 1 1 63DF6C9E
P 8875 2650
F 0 "#PWR014" H 8875 2550 50  0001 C CNN
F 1 "+VDC" H 8875 2900 50  0000 C CNN
F 2 "" H 8875 2650 50  0001 C CNN
F 3 "" H 8875 2650 50  0001 C CNN
	1    8875 2650
	0    1    1    0   
$EndComp
Wire Wire Line
	8775 2650 8875 2650
$Comp
L +VDC #PWR?
U 1 1 63DF8C38
P 9200 1825
F 0 "#PWR?" H 9200 1725 50  0001 C CNN
F 1 "+VDC" H 9200 2075 50  0000 C CNN
F 2 "" H 9200 1825 50  0001 C CNN
F 3 "" H 9200 1825 50  0001 C CNN
	1    9200 1825
	0    1    -1   0   
$EndComp
$Comp
L +VDC #PWR?
U 1 1 63DF8DA3
P 7850 1825
F 0 "#PWR?" H 7850 1725 50  0001 C CNN
F 1 "+VDC" H 7850 2075 50  0000 C CNN
F 2 "" H 7850 1825 50  0001 C CNN
F 3 "" H 7850 1825 50  0001 C CNN
	1    7850 1825
	0    -1   -1   0   
$EndComp
$EndSCHEMATC
