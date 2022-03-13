import numpy as np
import cv2

import argparse
import math


def tuple_type(strings):
    strings = strings.replace("(", "").replace(")", "")
    mapped_int = map(int, strings.split(","))
    return tuple(mapped_int)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")

ap.add_argument("-p", "--point", required = False, help = "points",  type=tuple_type)

args = vars(ap.parse_args())

image = cv2.imread(args["image"],0)
output = cv2.imread(args["image"],1)

cv2.imshow("Original image", image)
cv2.waitKey()

blurred = cv2.GaussianBlur(image,(5,5),0)

circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1.5, 300,
                             param1=40,param2=20,minRadius=0,maxRadius=200)

if circles is not None:
    # If there are some detections, convert radius and x,y(center) coordinates to integer
    circles = np.round(circles[0, :]).astype("int")
    radius = 0
    
    
    for (x, y, r) in circles:        
        radius = r
        cv2.circle(output, (x, y), r, (0,255,0), 3) 
        
        if args["point"] and len(args["point"]) == 2:
            center=(x,y)
            coordinate=args["point"]
            
            cv2.circle(output, args["point"], radius=0, color=(0, 0, 255), thickness=10)

            if (coordinate[0]-center[0])**2 + (coordinate[1]-center[1])**2 < radius**2:
                cv2.putText(output, 'Inside', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                1, (255, 0, 0), 2, cv2.LINE_AA)
            else:   
                cv2.putText(output, 'Outside', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                1, (255, 0, 0), 2, cv2.LINE_AA)
        
    
    cv2.imshow("circle_detection",output)
    cv2.waitKey()    
else:
    print("circle not detected")
