# -*- coding: utf-8 -*-
"""
Functions for data recording.
"""
import matplotlib.pyplot as plt
import re

def record_pressure_data(file_name, pressure_data, speed_data):
    file1 = open('Recorded_Data/' + file_name + "_pressure" + '.tsv', 'a')
    file2 = open('Recorded_Data/' + file_name + "_speed" + '.tsv', 'a')
    for i in range(6):
        file1.write(str(pressure_data[i]) + '\t')
        if i == 5:
            file1.write('\n')
    file1.close()
    for i in range(6):
        file2.write(str(speed_data[i]) + '\t')
        if i == 5:
            file2.write('\n')
    file2.close()
    
def record_intentional_angle(file_name, angle_data):
    file = open('Recorded_Data/' + file_name + '.tsv', 'a')
    file.write(str(angle_data) + '\n')
    file.close()
    
def log_to_path(file_name):
    """Write in path log data, produce a tsv data point file"""
    data_x = []
    data_y = []
    f = open('Recorded_Data/' + file_name + '.txt', 'w')
    line_index = 0
    for line in f:
        if "LE:0" in line:
            if line_index %  8== 0:
                pattern = re.compile(r'(\[.*?\])')
                match = re.findall(pattern, line)[0][1:-1].split(',')
                data_x.append(float(match[0]))
                data_y.append(float(match[1]))
            line_index += 1
    file = open('Recorded_Data/' + file_name + '.tsv', 'w')
    for i in range(len(data_x)):
        file.write(str(data_x[i]) + '\t')
        file.write(str(data_y[i]) + '\t')
        file.write('\n')
    file.close()