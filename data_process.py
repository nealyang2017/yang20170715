# -*- coding: utf-8 -*-
"""
Functions for data recording.
"""

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