#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 15:57:27 2017

@author: neal
"""
import Tkinter         
from PIL import Image, ImageTk  
import thread
import time
import math
from OmniDirectionalPlatform import *
from DistanceBasedFuzzyReasoning import *
import Algorithms as ag
import data_process as dp

def color_in_RGB(r, g, b):
    return "#%02x%02x%02x"%(r,g,b)

def purple_in_level(level):
    return color_in_RGB(222-level, 196-level, 238-level)

def draw_circle(point, radius, color, canvas):
    return canvas.create_oval(point[0]-radius, point[1]-radius, point[0]+radius, point[1]+radius, fill = color,outline = '')
    
def draw_angle_dot(angle):
    global angle_dot
    global angle_line
    global canvas
    
    point = [400+180*math.cos(math.radians(angle)),436-180*math.sin(math.radians(angle))] 
#    point = [400-180*math.sin(math.radians(angle)),256+180-180*math.cos(math.radians(angle))] 
    canvas.delete(angle_dot)
    canvas.delete(angle_line)
    angle_dot = draw_circle(point, 30, color_in_RGB(65, 173, 190), canvas)
    angle_line = canvas.create_line(400,436,point[0],point[1],fill = "red", width = "3",dash = (4, 4))
    canvas.pack()
   
def refresh():
    global angle_dot
    global angle_line
    global training_robot
    global sensor_RF
    global sensor_RR
    global sensor_RB
    global sensor_LF
    global sensor_LL
    global sensor_LB
    global canvas
    refresh_time = 0
#    intended_angle_box = [30, 35, 73, 131, 144, 100, 65]
#    intended_angle_box = [-90, -90, -60, -30, 0, 30, 60, 90]
#    intended_angle_box = [30, 35]
    init_pdf = ag.pdf(15, 1)
    intended_angle = 0
    while True:
#        refresh_time += 1
#        intended_angle = intended_angle_box[refresh_time // 100]
        training_robot.refresh_sensor_buffer()
        force_data = [training_robot.sensor_data_buffer[0][-1],
                      training_robot.sensor_data_buffer[1][-1],
                      training_robot.sensor_data_buffer[2][-1],
                      training_robot.sensor_data_buffer[3][-1],
                      training_robot.sensor_data_buffer[4][-1],
                      training_robot.sensor_data_buffer[5][-1]]
        speed_data = [training_robot.sensor_speed_buffer[0][-1],
                      training_robot.sensor_speed_buffer[1][-1],
                      training_robot.sensor_speed_buffer[2][-1],
                      training_robot.sensor_speed_buffer[3][-1],
                      training_robot.sensor_speed_buffer[4][-1],
                      training_robot.sensor_speed_buffer[5][-1]]
#        print force_data
#        fuzzy = DistanceBasedFuzzyReasoning()
#        fuzzy.read_knowleage_base('0704', 5)
#        (confidence, resulted_angle) = fuzzy.reasoning(force_data)
#        print confidence
        init_pdf = ag.speed_recognition(training_robot.sensor_speed_buffer, init_pdf)    
        intended_speed = init_pdf[0]
#        dp.record_pressure_data("diff_speed3", force_data, speed_data)
#        dp.record_intentional_angle("diff_speed3",  intended_speed)
#        instruction_label['text'] = str(intended_speed)
        
#        if confidence > 0.6:
#            intended_angle = resulted_angle
#        training_robot.speed = 9
#        training_robot.angle = intended_angle
#        file.write(str(resulted_angle))
#        file.write('\n')
#        file.close()
#        print str(intended_angle) + "," + str(resulted_angle - intended_angle)
#        instruction_label['text'] = str(intended_angle) + "........................." + "%.4f" % (resulted_angle - intended_angle)

#        file = open("Recorded_Data/dynamc1.tsv", 'a')
#        init_pdf = ag.speed_recognition(training_robot.sensor_speed_buffer, init_pdf)    
#        intended_direction = init_pdf[0]
#        if intended_direction > 30 or intended_direction < 0:
#            training_robot.speed = 0
#        else:
#            training_robot.speed = intended_direction
#        ag.plot_pdf(init_pdf)
#        file.write(str(speed_intention))
#        file.write('\n')
#        file.close()
#        instruction_label['text'] =  str(intended_direction)




root = Tkinter.Tk()
#canvas = Tkinter.Canvas(root, width = 800, height = 650, bg = 'white')  
instruction_label = Tkinter.Label(root, text='Please press "Start" button!',font = 'Times 50', height = 2)
instruction_label.grid(row=1, column=1, columnspan=6)
#background_pic = Image.open("bg.gif")  
#background_img = ImageTk.PhotoImage(background_pic) 
#canvas.create_image(400,350,image = background_img)    
#
#angle_dot = draw_circle([400,350], 30, color_in_RGB(65, 173, 190), canvas)
#angle_line = canvas.create_line(400,436,400,350,fill = "red", width = "3",dash = (4, 4))
#
#sensor_LL = draw_circle([70,203], 50, purple_in_level(0), canvas) 
#sensor_LB = draw_circle([70,353], 50, purple_in_level(0), canvas) 
#sensor_RR = draw_circle([728,203], 50, purple_in_level(0), canvas) 
#sensor_RB = draw_circle([728,353], 50, purple_in_level(0), canvas)
#sensor_LF = draw_circle([241,100], 50, purple_in_level(0), canvas)
#sensor_RF = draw_circle([572,100], 50, purple_in_level(0), canvas)
#instrument_board = draw_circle([400,436], 180, color_in_RGB(215, 213, 220), canvas)
#canvas.pack()

training_robot = OmniDirectionalPlatform(['COM11', 115200], 'diff_speed1_pressure')

thread.start_new_thread(refresh,())  
root.mainloop() 