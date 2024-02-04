#!/usr/bin/python3

''' 
Code to detect and follow a color 
    
Run the color_detection launch commands before this file 

Execute with python3 color_detection.py 

Complete this template and the template files color_image and velocity
'''

# Import libraries
########################################################################
import cv2
import numpy as np 
import rospy
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from color_image import show_image, get_color_range, detect_color, get_max_contour
from velocity import get_velocity


# Variables 
########################################################################
bridge = CvBridge()
min_detection = 30000



# Image callback -> it is called when the topic receives information
################################################################
def image_callback(msg):
    
    rospy.loginfo("Image received")

    # Get image and publisher 
    ##########################################

    # Convert your ros image message to opencv using bridge
    img = bridge.imgmsg_to_cv2(msg, "bgr8")

    # Show image using show_image function
    show_image(img, "window_name")

    # Get half width of the image 
    mid_width = img.shape[1] // 2

    # Create velocity publisher and variable of velocity
    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel = Twist()

    
    # Do color detection 
    ##########################################

    # Get color range using get_color_range from color_image.py
    lower_range, upper_range = get_color_range('red')
    
    # Get color mask using detect_color from color_image.py
    mask = detect_color(img, lower_range, upper_range)

    # Show mask 
    show_image(mask, "Color Mask")

    # Find contours and get max area using get_max_contours from color_image.py 
    contours, area, center = get_max_contour(mask)
    print("Maximum area: ", area)


    # Get robot speed     
    ##########################################

    # If the area of the detected color is big enough
    if area > min_detection:
        print("Cylinder detected")

        # Draw contour and center of the detection and show image 
        cv2.drawContours(img, [contours], 0, (0, 255, 0), 3)
        cv2.circle(img, center, 5, (0, 0, 255), -1)
        show_image(img, "Detected Color")

        # Gets the color speed and direction depending on the color detection using get_velocity from velocity.py
        linear_vel, angular_vel = get_velocity(vel, area, center[0], mid_width)
        vel.linear.x = linear_vel
        vel.angular.z = angular_vel

            
    # If the area of the detected color is not big enough, the robot spins 
    else:
        print("Looking for color: spinning")
        vel.angular.z = 0.1
        

    # Publish velocity
    vel_pub.publish(vel)




# Init node and suscribe to image topic 
################################################################
def main():
    # Init node 'color_detection'
    rospy.init_node('color_detection')

    # Suscribe to image topic and add callback + spin
    rospy.Subscriber("/camera/rgb/image_raw" , Image , image_callback)
    rospy.spin()    
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()