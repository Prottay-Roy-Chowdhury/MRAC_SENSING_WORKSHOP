#!/usr/bin/python3

'''
FUNCTIONS FOR COLOR DETECTION CODE
'''

import cv2 

# Resize and show image 
def show_image(img, window_name): 
    img_res = cv2.resize(img, None, fx=0.3, fy=0.3)
    cv2.imshow(window_name, img_res)
    cv2.waitKey(1)


# Get color limits
def get_color_range(color):
    
    # Complete only for the color you want to detect 

    if(color == 'red'):
        lower_range = (0, 50, 50)
        upper_range = (10, 255, 255)
 
    #elif(color == 'green'):
    #    lower_range = # <COMPLETE>
    #    upper_range = # <COMPLETE>

    #elif(color == 'blue'):
    #    lower_range = # <COMPLETE>
    #    upper_range = # <COMPLETE>

    #else: # Yellow 
    #    lower_range = # <COMPLETE>
    #    upper_range = # <COMPLETE>
    
    return lower_range, upper_range



# Detects the color 
def detect_color(img, lower_range, upper_range):

    # Perform a Gaussian filter 
    img_gauss = cv2.GaussianBlur(img, (5, 5), 0)

    # Convert gauss image to HSV
    img_hsv = cv2.cvtColor(img_gauss, cv2.COLOR_BGR2HSV)

    # Get color mask
    color_mask = cv2.inRange(img_hsv, lower_range, upper_range)

    # Define rectangular kernel 25x25
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))

    # Apply openning to mask 
    mask = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, kernel)

    return mask



# Get maximum contour, area and its center 
def get_max_contour(mask): 

    contour_max = []
    area_max = 0
    center = (-1,-1)

    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # For each contour
    for contour in contours:
    
        # Get area of the contour 
        area = cv2.contourArea(contour)

        # If area is bigger than area_max 
        if area > area_max:
            # Update area max value 
            area_max = area

            # Update contour_max value
            contour_max = contour

            # Get center of the contour using cv2.moments
            moments = cv2.moments(contour)
            center = (int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00']))


    return contour_max, area_max, center