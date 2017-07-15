"""Algorithms Functions."""

from LoadSensorTsvFile import *
import numpy as np
import matplotlib.pyplot as plt 
import math

def calc_peak_width(load_speed):
    """Calculate the nearest passed peak width."""
    #Find zero crossing points index.
    zero_cross_index = []
    for index in range(len(load_speed)):
        if index == len(load_speed) - 1:
            pass
        elif load_speed[index] == 0:
            zero_cross_index.append(index)
        elif load_speed[index] * load_speed[index + 1] < 0:
            zero_cross_index.append(index)
#    print zero_cross_index
#    walking_power = sum(data for data in load_speed[zero_cross_index[-2]: zero_cross_index[-1]])
    #Calculate the derivative of zero crossing points.

    space = 0
    index = -1
    while space <= 0:
        space = sum(data for data in load_speed[zero_cross_index[index-1]: zero_cross_index[index]])
#        for i in range(zero_cross_index[index-1], zero_cross_index[index]):
#            space += load_speed[i]  
        index -= 1
        if index < -40:
            break
#        print space
    if space < 5 or space > 100:
        return 0
    peak_width = zero_cross_index[index+1] - zero_cross_index[index]
    return [peak_width, space]

def calc_moving_power(load_speed):
    """Calculate the current moving power in order to be certain
       whether the load sensor is considered active.
    """
    return sum([data * data for data in load_speed])

def speed_recognition(load_speed, init_pdf):
    """Recognize the user speed from load variation speed data.
       LOAD_SPEED is a list of size 50.
    """
    peak_feature = [0] * 6 
    for i in range(6):
        peak_feature[i] = calc_peak_width(load_speed[i])
#        moving_power[i] = calc_moving_power(load_speed[i])
    print peak_feature
    for feature in peak_feature:
        if feature == 0:
            pass
        else:
            cur_pdf = pdf(feature[0], 200.0 / feature[1])
            init_pdf = add_gaussian_function(init_pdf, cur_pdf)
    return init_pdf
 
#    print np.mean(peak_width)

def guassian_function(x, m, s):
    return 1/(math.sqrt(2*math.pi)*s) * math.exp(-math.pow(x-m,2)/(2*math.pow(s,2)))

def pdf(m, s):
    return [m, s]

def add_gaussian_function(pdf1, pdf2):
    m = (pdf1[0]*pdf2[1]*pdf2[1] + pdf2[0]*pdf1[1]*pdf1[1]) / (pdf1[1]*pdf1[1] + pdf2[1]*pdf2[1])
    s = math.sqrt(float(pdf1[1]*pdf1[1]*pdf2[1]*pdf2[1]) / (pdf1[1]*pdf1[1] + pdf2[1]*pdf2[1]))
    return pdf(m, s)
    
def plot_pdf(pdf):
    """"""
    x = np.arange(0, 10, 0.2)
    y = []
    for i in x:
        y.append(guassian_function(i, pdf[0], pdf[1]))
    plt.plot(x, y)


##Test
#pdf1 = [4, 1]
#pdf2 = [6, 6]
#pdf = add_gaussian_function(pdf1, pdf2)
#print pdf
#plot_pdf(pdf)

#tsv_file = LoadSensorTsvFile()
#tsv_file.read_in_file('Recorded_Data/diff_speed2.xls_speed2.tsv')
##one_row = tsv_file.files_data[0][2]
#speed_recognition(tsv_file.files_data[0])