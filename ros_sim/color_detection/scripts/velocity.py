#!/usr/bin/python3

import cv2 

# Variables 
########################################################################
max_area_detection = 30000
min_area_detection = 15000




# Functions 
########################################################################

# Gets the robot speed and direction depending on the color detection 
def get_velocity(vel, area, x, mid_width):
    linear_vel = 0.0
    angular_vel = 0.0    

    #########################################################################################
    # If the area is too big, robot too close --> the robot go backwards                    #
    # If the area is too small, robot far --> the robot go towards the color                #
    # If the area is between min_area_detection and max_area_detection --> the robot stops  # 
    #########################################################################################

    # if too close -> go backwards
    if area > max_area_detection:
        linear_vel = -0.5

    # if too far -> move towards
    elif area < max_area_detection:
        linear_vel = 0.5

        # The robot will turn to the color to keep the detection in the middle of the image 
        # Use get_angular_velocity to get the robot to spin towards the color   
        angular_vel = get_angular_velocity(x, mid_width)
        
    
    # if good distance --> stop
    else:
        linear_vel = 0.0
        angular_vel = 0.0   
    

    return linear_vel, angular_vel



# Gets the angular velocity if the color detection is on one side of the image to turn towards the color 
# x : x coordenate of the centroid of the color 
# mid_width : middle width of image 
def get_angular_velocity(x, mid_width):
    vel_z = 0.0
    offset = 20
    
    # If the centroid of the color is on the right part of the image + offset
    if x > mid_width + offset:
        # Turn to the right
        vel_z = -0.1

    # If the centroid of the color is on the left part of the image - offset
    elif x < mid_width - offset:
        # Turn to the left
        vel_z = 0.1

    return vel_z