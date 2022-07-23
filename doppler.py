#!/usr/bin/env python3
#####################################################

# Ops241A module settings:  mph, dir off, 20Ksps, min -9dB pwr, squelch 5000
Ops241A_Speed_Output_Units = 'US'
Ops241A_Direction_Control = 'Od'
Ops241A_Sampling_Frequency = 'S2'
Ops241A_Transmit_Power = 'PX'
Ops241A_Threshold_Control = 'QI'
Ops241A_Module_Information = '??'
Ops241A_Data_Accuracy = 'F1'
display_max_speed_time = 1
reset_speed_time = 5

#####################################################
# Import time, decimal, serial, GPIO, reg expr, sys, and pygame modules
import os
import sys
from time import *
from decimal import *
import serial
import RPi.GPIO as GPIO
import re

# Initialize the USB port to read from the OPS-241A module
ser=serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1,
    writeTimeout = 2
)
ser.flushInput()
ser.flushOutput()

# sendSerialCommand: function for sending commands to the OPS-241A module
def sendSerCmd(descrStr, commandStr) :
    data_for_send_str = commandStr
    data_for_send_bytes = str.encode(data_for_send_str)
    print(descrStr, commandStr)
    ser.write(data_for_send_bytes)
    # Initialize message verify checking
    ser_message_start = '{'
    ser_write_verify = False
    # Print out module response to command string
    while not ser_write_verify :
        data_rx_bytes = ser.readline()
        data_rx_length = len(data_rx_bytes)
        if (data_rx_length != 0) :
            data_rx_str = str(data_rx_bytes)
            if data_rx_str.find(ser_message_start) :
                print(data_rx_str)
                ser_write_verify = True
            
# Initialize and query Ops241A Module
print("\nInitializing Ops241A Module")
sendSerCmd("\nSet Speed Output Units: ", Ops241A_Speed_Output_Units)
sendSerCmd("\nSet Direction Control: ", Ops241A_Direction_Control)
sendSerCmd("\nSet Sampling Frequency: ", Ops241A_Sampling_Frequency)
sendSerCmd("\nSet Transmit Power: ", Ops241A_Transmit_Power)
sendSerCmd("\nSet Threshold Control: ", Ops241A_Threshold_Control)
sendSerCmd("\nSet Data Accuracy: ", Ops241A_Data_Accuracy)
sendSerCmd("\nModule Information: ", Ops241A_Module_Information)


ser=serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 0.01,
    writeTimeout = 2
    )

# Speed limit display loop
done = False
# Flush serial buffers
ser.flushInput()
ser.flushOutput()
# Reset timers
start_time = time()
current_time = start_time
delta_time = 0.0
speed_max = 0.0
while not done:
    # Check for speed info from OPS241-A
    speed_available = False
    Ops241_rx_bytes = ser.readline()
    Ops241_rx_bytes_length = len(Ops241_rx_bytes)
    if (Ops241_rx_bytes_length != 0) :
        Ops241_rx_str = str(Ops241_rx_bytes)
        if Ops241_rx_str.find('{') == -1 :
            # Speed data found
            Ops241_rx_float = float(Ops241_rx_bytes)
            speed_available = True
    if speed_available == True :
        print('speed is:', Ops241_rx_float)
        if Ops241_rx_float > speed_max :
            speed_max = Ops241_rx_float
            start_time = time()
            current_time = start_time
        else :
            current_time = time()
            delta_time = current_time - start_time
            if delta_time > display_max_speed_time :
                speed_max = Ops241_rx_float
                start_time = time()
                current_time = start_time
    else :
        current_time = time()
        delta_time = current_time - start_time
        # Reset speed limit to zero if no motion detected after reset_speed_time
        if delta_time > reset_speed_time :
            print('no speed detected, resetting to 0')
            start_time = time()
            current_time = start_time
