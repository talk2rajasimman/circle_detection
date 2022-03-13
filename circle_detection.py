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
        cv2.rectangle(output, (x - 2, y - 2), (x + 2, y + 2), (0,255,0), -1)
    
    if args["point"] and len(args["point"]) == 2:
        
        points = args["point"]
        x = points[0]
        
        y = points[1]        
        polarradius = math.sqrt(x * x + y * y)
        
        if polarradius < radius:
        
            cv2.putText(output, 'Inside', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                            1, (255, 0, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(output, 'Outside', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                            1, (255, 0, 0), 2, cv2.LINE_AA)
    
    cv2.imshow("circle_detection",output)
    cv2.imwrite("4.jpg",output)
    cv2.waitKey()    
else:
    print("Circle Not Found")