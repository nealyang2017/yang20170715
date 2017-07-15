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
   
    while True:
        
        training_robot.refresh_sensor_buffer()
        force_data = [training_robot.sensor_data_buffer[0][-1],
                      training_robot.sensor_data_buffer[1][-1],
                      training_robot.sensor_data_buffer[2][-1],
                      training_robot.sensor_data_buffer[3][-1],
                      training_robot.sensor_data_buffer[4][-1],
                      training_robot.sensor_data_buffer[5][-1]]
#        print force_data
        file = open("Recorded_Data/diff_speed3.tsv", 'a')
        for i in range(6):
            file.write(str(force_data[i]) + '\t')
        file.write('\n')
        file.close()
        speed_intention = ag.speed_recognition(training_robot.sensor_speed_buffer)
        if speed_intention > 3 :
                print  int(1.0 / speed_intention * 89)
                training_robot.speed = int(1.0 / speed_intention * 100)
                fuzzy = DistanceBasedFuzzyReasoning()
                fuzzy.read_knowleage_base('0704', 5)
                intentiona_angle = fuzzy.reasoning(force_data)
#            print intentiona_angle
                draw_angle_dot(intentiona_angle) 
#            training_robot.speed = 5
                training_robot.angle = intentiona_angle 


#        if sum(list(map(lambda x: x[0]-x[1], zip(force_data, [1000]*6)))) < 30:
#            training_robot.speed = 0
#            canvas.delete(angle_dot)
#            canvas.delete(angle_line)
#            angle_dot = draw_circle([400,436], 30, color_in_RGB(65, 173, 190), canvas)
#        else:
#            
#            fuzzy = DistanceBasedFuzzyReasoning()
#            fuzzy.read_knowleage_base('0704', 5)
#            intentiona_angle = fuzzy.reasoning(force_data)
##            print intentiona_angle
#            draw_angle_dot(intentiona_angle) 
#            training_robot.speed = 10
#            training_robot.angle = intentiona_angle 
##            training_robot.angle = 0
        
        
        sensor_LL = draw_circle([70,203], 50, purple_in_level((training_robot.sensor_data_buffer[4][-1]-997)/2), canvas) 
        sensor_LB = draw_circle([70,353], 50, purple_in_level((training_robot.sensor_data_buffer[5][-1]-997)/2), canvas) 
        sensor_RR = draw_circle([728,203], 50, purple_in_level((training_robot.sensor_data_buffer[1][-1]-997)/2), canvas) 
        sensor_RB = draw_circle([728,353], 50, purple_in_level((training_robot.sensor_data_buffer[2][-1]-997)/2), canvas)
        sensor_LF = draw_circle([241,100], 50, purple_in_level((training_robot.sensor_data_buffer[3][-1]-997)/2), canvas)
        sensor_RF = draw_circle([572,100], 50, purple_in_level((training_robot.sensor_data_buffer[0][-1]-997)/2), canvas)
#        sensor_RF = draw_circle([572,100], 50, purple_in_level((training_robot.sensor_data_buffer[0][-1]-997)), canvas)
        canvas.pack()
        
#    for j in range(5):
#        i = 0
#        while i < 360:
#            draw_angle_dot(i) 
#            time.sleep(0.06)
#            i +=6


root = Tkinter.Tk()
canvas = Tkinter.Canvas(root, width = 800, height = 650, bg = 'white')  
background_pic = Image.open("bg.gif")  
background_img = ImageTk.PhotoImage(background_pic) 
canvas.create_image(400,350,image = background_img)    

angle_dot = draw_circle([400,350], 30, color_in_RGB(65, 173, 190), canvas)
angle_line = canvas.create_line(400,436,400,350,fill = "red", width = "3",dash = (4, 4))

sensor_LL = draw_circle([70,203], 50, purple_in_level(0), canvas) 
sensor_LB = draw_circle([70,353], 50, purple_in_level(0), canvas) 
sensor_RR = draw_circle([728,203], 50, purple_in_level(0), canvas) 
sensor_RB = draw_circle([728,353], 50, purple_in_level(0), canvas)
sensor_LF = draw_circle([241,100], 50, purple_in_level(0), canvas)
sensor_RF = draw_circle([572,100], 50, purple_in_level(0), canvas)
instrument_board = draw_circle([400,436], 180, color_in_RGB(215, 213, 220), canvas)

canvas.pack()

training_robot = OmniDirectionalPlatform(['COM11', 115200])

thread.start_new_thread(refresh,())  
root.mainloop() 