#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 09:38:22 2017

@author: neal
"""
import csv

class LoadSensorTsvFile:
    """
    """
    def __init__(self):
        self.files_data = []
        self.feature = []
        
        pass
    
    def read_in_file(self, file):    
        csv_reader = csv.reader(open(file))
        file_data = [[0]*51]*7
        row_num = 0
        for row in csv_reader:
            file_data[row_num] =  row[0].split('\t')
            del file_data[row_num][-1]
            for i in range(len(file_data[row_num])):
                file_data[row_num][i] = float(file_data[row_num][i])
            row_num += 1
#        print file_data
        self.files_data.append(file_data)

    
    def read_in_files(self, file_path=""):
        """
        file_path: Folder containing data files
        """
        files = []
        for i in range(8):
            files.append(file_path + "/direction_" + str(i+1) + ".tsv")
        for file in files:
            self.read_in_file(file)
    
    def get_feature(self, feature_func, slice_range=[23, 28]):
        """
        """
        for file_data in self.files_data:
            feature_func(file_data, slice_range)
#        print self.feature
    
    def slice_avg(self, file_data, slice_range):
        """Calculate the average value of a slice of the data
        """
        row_num = 0
        feature_data = [0] * 7
        for row in file_data:
            feature_data[row_num] = sum(row[slice_range[0]:slice_range[1]]) / (slice_range[1] - slice_range[0])
            row_num += 1
        self.feature.append(feature_data)
    
#tsv_file = LoadSensorTsvFile()
#tsv_file.read_in_files('050801_yangguang')
#tsv_file.get_feature(tsv_file.slice_avg)
