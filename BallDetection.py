import cv2 as cv
from math import atan, degrees
import numpy as np
import json

with open('camera.json', 'r') as jsonfile:
    camera_data = json.load(jsonfile)
mtx = np.array(camera_data['mtx'])
dist = np.array(camera_data['dist'])
ball_width = 0.4

def BallDetection(img, canva, team_color):
    imgc = np.copy(img)
    blurred = cv.GaussianBlur(imgc, (11, 11), 0)
    hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
    
    if (team_color == 'red'):
        lThreshold = np.array([0, 150, 150])
        hThreshold = np.array([30, 255, 255])
    else:
        lThreshold = np.array([100, 100, 150])
        hThreshold = np.array([255, 255, 255])
        
    mask = cv.inRange(hsv, lThreshold, hThreshold)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)
    only_tc = cv.bitwise_and(img, img, mask=mask)
    gray = cv.cvtColor(only_tc, cv.COLOR_BGR2GRAY)
    
    cv.imshow('threshold', mask)
    
    #-----------------------------------------------------------#
    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    # undistort
    gray = cv.undistort(gray, mtx, dist, None, newcameramtx)
    #----------------------------------------------------------#
    # Method-1
    
    # circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 50)
    
    # if circles is not None:
    #     print('has found!')
    #     circles = np.round(circles[0, :]).astype(int)
        
    #     for (x, y, r) in circles:
    #         cv.circle(canva, (x, y), r, (0, 255, 0), 4)
    #         cv.circle(canva, (x, y), 3, (0, 255, 255))
            
    #----------------------------------------------------------#
    # Method-2
    
    cnts, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    distance, angle= -1, -1
    
    for cnt in cnts:
        cntArea = cv.contourArea(cnt)
        if cntArea > 100:
            ((x, y), r) = cv.minEnclosingCircle(cnt)
            cA = r**2*np.pi
            # M = cv.moments(cnt)
            # center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))
            if r > 15 and cntArea > cA*.7:
                cv.circle(canva,(int(x), int(y)), int(r), (0, 255, 0), 3)
                # Different object has its different factors
                # for 640*480
                if cv.waitKey(1) == ord('p'):
                    print(2*r)
                    print(x-320)
                # r is the radius calculated by pixel
                # x is the coordinate in 2D
                distance  =  (ball_width * 3375) / r
                hdis = (x-320)*5/138 * distance / 20
                angle = degrees(atan(hdis/distance))
                
                print('dis:',distance, 'angle', angle, end='\r')
            # cv.drawContours(canva, cnt, -1, (0, 255, 0), 3)
    #----------------------------------------------------------#
    
    output = [distance, angle]
    return output

if __name__ == '__main__':
    import Demo
    Demo.main()