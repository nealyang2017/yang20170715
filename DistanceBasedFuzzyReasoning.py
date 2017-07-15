#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 22:31:10 2017

@author: neal
"""
import math
from LoadSensorTsvFile import *
import numpy as np
import matplotlib.pyplot as plt

class DistanceBasedFuzzyReasoning:
    """
    """
    def __init__(self, A_ij=[], B_i = [0, 45, 90, 135, 180, 225, 270, 315]):
        """
        """
        self.A_ij = A_ij
        self.B_i = B_i
        
    def read_knowleage_base(self, file_path, bias):
        """ Read the knowleage base from a file
        """ 
        tsv_file = LoadSensorTsvFile()
        tsv_file.read_in_files(file_path)
        tsv_file.get_feature(tsv_file.slice_avg)
#        print tsv_file.feature
        
        # Wired situation, 
        A_ij_row = []
        for row_num in range(8):
            for col_num in range(6):
                A_ij_row.append( [tsv_file.feature[row_num][col_num + 1] - bias,
                                          tsv_file.feature[row_num][col_num + 1],
                                          tsv_file.feature[row_num][col_num + 1] + bias])
            self.A_ij.append(A_ij_row)
            A_ij_row = []
#            print A_ij_row
#        print self.A_ij

    def calc_distance_ij(self, A_ij=[0, 0, 0], A_j=0): 
        """
        """
        # Method 1
#        distance_ij = (math.sqrt((A_ij[0]-A_j)**2 + (A_ij[1]-A_j)**2 + abs(A_ij[0]-A_j)*abs(A_ij[1]-A_j))
#        + math.sqrt((A_ij[1]-A_j)**2 + (A_ij[2]-A_j)**2 + abs(A_ij[1]-A_j)*abs(A_ij[2]-A_j))) / math.sqrt(3)
#        return distance_ij
        # Method 2
        distance_ij = (A_j - A_ij[1])**2
        return distance_ij 
    
    def calc_distance_i(self, rule_number, force_data):
        """
        """
        distance_i = 0.0
        for sensor_num in range(6):
            distance_i += self.calc_distance_ij(self.A_ij[rule_number][sensor_num], force_data[sensor_num])
#        print distance_i
        return distance_i
        
        
    def reasoning(self, force_data):
        """
        """
        # Calculate num
#        num = 0.0
#        for i in range(8):
#            temp = self.B_i[i]
#            for rule_number in range(8):
#                if i != rule_number:
#                    temp = temp * self.calc_distance_i(rule_number, force_data)
#            num += temp
        mod = [1] * 8
        for i in range(8):
            for rule_number in range(8):
                if i != rule_number:
                    mod[i] = mod[i] * self.calc_distance_i(rule_number, force_data)
        # Calculate den
        den = 0.0
        for i in range(8):
            temp = 1.0
            for rule_number in range(8):
                if i != rule_number:
                    temp = temp * self.calc_distance_i(rule_number, force_data)
            den += temp
        
        for i in range(8):
            mod[i] = mod[i]/den
        
#        print mod
        angle = [0,0]
        for i in range(8):
            angle[0] += mod[i] * math.cos(self.B_i[i]/180.0*3.14)
            angle[1] += mod[i] * math.sin(self.B_i[i]/180.0*3.14)
#        self.plot_radar(mod)
#        return (math.sqrt(angle[0]**2 + angle[1]**2), math.atan2(angle[1],angle[0]) / 3.14 * 180)
#        print [math.sqrt(angle[0]**2 + angle[1]**2), math.atan2(angle[1],angle[0]) / 3.14 * 180]
        return math.atan2(angle[1],angle[0]) / 3.14 * 180
    def plot_radar(self, values=[0]*8):
        # Compute pie slices
        radii = values
        N = 8
        theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
        width = [0.5] * N
        fig = plt.gcf()
#        fig.set_size_inches(1.69, 1.69)     # Size for saving
        fig.set_size_inches(5, 5)        # Size for showing
        ax = plt.subplot(111, projection='polar')
        ax.set_thetagrids([0, 45, 90, 135, 180, 225, 270, 315], fontsize = 8)
        ax.set_rgrids([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],fontsize = 7)
        bars = ax.bar(theta, radii, width=width, bottom=0.0)
        
        # Use custom colors and opacity
        for r, bar in zip(radii, bars):
            bar.set_facecolor(plt.cm.viridis(r / 0.55))
            bar.set_alpha(0.5)
        plt.show()
        
    def plot_single_direction_info(self, file_name):
        tsv_file = LoadSensorTsvFile()
        tsv_file.read_in_file(file_name)
        sample = 99
        #print tsv_file.files_data[0][1]
        length = [0] * sample
        angle = [0] * sample
        for i in range(sample):
            force_data = [tsv_file.files_data[0][1][i], tsv_file.files_data[0][2][i], tsv_file.files_data[0][3][i],
                          tsv_file.files_data[0][4][i], tsv_file.files_data[0][5][i], tsv_file.files_data[0][6][i]]
            (length[i], angle[i]) = fuzzy.reasoning(force_data)
            length[i] = length[i]
        x1 = np.linspace(0, 200, sample)
        x2 = np.linspace(0, 200, sample)
        y1 = angle
        y2 = length
        fig = plt.gcf()
        fig.set_size_inches(3.4, 3.4)  
        plt.subplot(2, 1, 1)
        plt.plot(x1, y1, 'o-')
        plt.title('A tale of 2 subplots', fontsize = 10)
        plt.ylabel('Angle')
        
        plt.subplot(2, 1, 2)
        plt.plot(x2, y2, '.-')
        plt.xlabel('time (s)', fontsize = 10)
        plt.ylabel('Belief')
        
#            x = np.linspace(0, 49, 50)
#            fig, ax = plt.subplots()
#            line1, = ax.plot(x, length, '--')
#            line2, = ax.plot(x, angle, )
        plt.show()
  
# Test 

#fuzzy = DistanceBasedFuzzyReasoning()
#fuzzy.read_knowleage_base('0704', 15)
#fuzzy.plot_single_direction_info('Recorded_Data/diff_direction.tsv')

#for i in range(8):
#    print fuzzy.calc_distance_i(i, force_data)
#result = fuzzy.reasoning(force_data)
#print result
