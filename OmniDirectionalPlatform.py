#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 18:37:47 2017

@author: neal
"""
import math
import serial
import time

class OmniDirectionalPlatform:
    def __init__(self, serial_port, simulation_file='', buffer_size=50):
        """Open serialport and initiate sensor data buffer.
        
        Args:
            serial_port: Serialport number and baudrate
            simulation_file: .tsv pressure data for the simulation 
            buffer_size: Buffer size of the data buffer
            
        Raises:
            Except: Print error info when serial port opening operation is failed.
        """
        self.serial_port = serial_port
        self.angle = 0
        self.speed  = 0
        self.buffer_size = buffer_size
        self.sensor_bias = [617, 638, 320, 324, 801, 503]
        
        self.time_data = [0] * self.buffer_size    #Time stamps
        self.sensor_data_buffer = [[0] * self.buffer_size, [0] * self.buffer_size, [0] * self.buffer_size,
                            [0] * self.buffer_size, [0] * self.buffer_size, [0] * self.buffer_size]
        self. sensor_speed_buffer = [[0] * self.buffer_size, [0] * self.buffer_size, [0] * self.buffer_size,
                            [0] * self.buffer_size, [0] * self.buffer_size, [0] * self.buffer_size]
        if simulation_file != '':
            self.simulation_data = open('Recorded_Data/' + simulation_file + '.tsv', 'r')
            self.simulation = 1
        else:
            self.simulation = 0
        try:
            self.ser = serial.Serial(port=serial_port[0], baudrate=serial_port[1])
        except:
            print 'Cant open serial port' + self.serial_port[0]
           
    def motion_control(self, angle=0.0, speed=0, rotation=0):
        """Control the platform movements with serial port.
        
        Args:
            angle: Moving direction
            speed: Speed on the direction
            rotation: Speed of the rotation movement
        
        """
        data = [0] * 21        # Data to be sent with serial port
        data[0] = 0x01
        data[13] = 0x30
        data[14] = 0x32
        data[15] = 0x30
        data[16] = 0x30
        data[19] = 0x0d
        data[20] = 0x0a
        arc = angle * 0.01745
        speed_x = speed * math.cos(arc)
        speed_y = speed * math.sin(arc)
        w1 = int(0 - speed_x * 0.707 - speed_y * 0.707 + 0.5 * rotation)
        w2 = int(0 - speed_x * 0.707 + speed_y * 0.707 + 0.5 * rotation)
        w3 = int(speed_x * 0.707 - speed_y * 0.707 + 0.5 * rotation)
        w4 = int(speed_x * 0.707 + speed_y * 0.707 + 0.5 * rotation)
        if (w1 > 0):
            data[1] = 0x33
            data[2] = 0x30|((0xf0 & w1) >> 4)
            data[3] = 0x30 | (0x0f & w1)
        else:
            if (w1 != 0):
                w1 = 0 - w1
                data[1] = 0x31
                data[2] = 0x30 | ((0xf0 & w1) >> 4)
                data[3] = 0x30 | (0x0f & w1)
            else:
                data[1] = 0x30
                data[2] = 0x30
                data[3] = 0x30
        if (w2 > 0):
            data[4] = 0x33
            data[5] = 0x30 | ((0xf0 & w2) >> 4)
            data[6] = 0x30 | (0x0f & w2)
        else:
            if (w2 != 0):
                w2 = 0 - w2
                data[4] = 0x31
                data[5] = 0x30 | ((0xf0 & w2) >> 4)
                data[6] = 0x30 | (0x0f & w2)
            else:
                data[4] = 0x30
                data[5] = 0x30
                data[6] = 0x30
        if (w3 > 0):
            data[7] = 0x33
            data[8] = 0x30 | ((0xf0 & w3) >> 4)
            data[9] = 0x30 | (0x0f & w3)
        else:
            if (w3 != 0):
                w3 = 0 - w3
                data[7] = 0x31
                data[8] = 0x30 | ((0xf0 & w3) >> 4)
                data[9] = 0x30 | (0x0f & w3)
            else:
                data[7] = 0x30
                data[8] = 0x30
                data[9] = 0x30
        if (w4 > 0):
            data[10] = 0x33
            data[11] = 0x30 | ((0xf0 & w4) >> 4)
            data[12] = 0x30 | (0x0f & w4)
        else:
            if (w4 != 0):
                w4 = 0 - w4
                data[10] = 0x31
                data[11] = 0x30 | ((0xf0 & w4) >> 4)
                data[12] = 0x30 | (0x0f & w4)
            else:
                data[10] = 0x30
                data[11] = 0x30
                data[12] = 0x30
        # Create FCS part of the data
        fcs = 0
        for data_n in range(17):
            fcs = fcs ^ data[data_n]
        data[17] = ((fcs & 0xf0) >> 4) | 0x30
        data[18] = (fcs & 0x0f) | 0x30
        # Send data
        for i in range(21):
            self.ser.write(chr(data[i]))
        
    def refresh_sensor_buffer(self):
        """Read in new sensor data into data buffer
        """

        if self.simulation == 0:
            # Real operation mode(biad needed)
            # Send some data in order to recieve info
            for i in range(3):
                self.motion_control(self.angle, self.speed, 0)
            # Read sensor data
            sensor_data = self.ser.readline()
    #         Add new speed into the buffer
            for i in range(6):
                self.sensor_speed_buffer[i].append(int(sensor_data[(6 + i * 6) : (10 
                                       + i * 6)]) - self.sensor_bias[i] - self.sensor_data_buffer[i][-1])
                del self.sensor_speed_buffer[i][0]
            # Add new data into the buffer
            for i in range(6):
                self.time_data.append(time.clock())
                del self.time_data[0]
                self.sensor_data_buffer[i].append(int(sensor_data[(6 + i * 6) : (10 + i * 6)]) - self.sensor_bias[i])
                del self.sensor_data_buffer[i][0]
        else:
            # Simulatio mode(no bias needed)
            new_line = self.simulation_data.readline().split('\t') # Read in a line of data file per time
            # Recieve speed data
            for i in range(6):
                self.sensor_speed_buffer[i].append(int(new_line[i]) - self.sensor_data_buffer[i][-1])
                del self.sensor_speed_buffer[i][0]
            # Recieve pressure data
            for i in range(6):
                self.sensor_data_buffer[i].append(int(new_line[i]))
#                print self.simulation_data.readline().split('\t')[i]
                del self.sensor_data_buffer[i][0]
    

    def save_to_file(self, file_name, data_size=50):
        """Save certain size of data buffer into csv format
        
        """
        file = open(file_name, 'w')
        # Write the time stamp one row 1
        for i in range(data_size):
            file.write(str(self.time_data[i]) + '\t')
            if i == data_size - 1:
                file.write('\n')
        # Write sensor data in 6 rows
        for i in range(6):
            for j in range(data_size):
                file.write(str(self.sensor_data_buffer[i][j]) + '\t')
                if j == data_size - 1:
                    file.write('\n')
        file.close()
   
#robot = OmniDirectionalPlatform(['COM10', 115200])
#robot.speed = 5
#robot.angle = 0
#for i in range(300):
#    robot.refresh_sensor_buffer()
    