from cscore import CameraServer
from networktables import NetworkTables

import cv2 as cv
import numpy as np
import time
import json

import Apriltag


def main():
    with open('camera.json', 'r') as jsonfile:
        camera_data = json.load(jsonfile)

    width = camera_data['width']
    height = camera_data['height']
    fps = camera_data['fps']
    mtx = np.array(camera_data['mtx'])
    dist = np.array(camera_data['dist'])
    
    CameraServer.enableLogging()

    camera = CameraServer.startAutomaticCapture(0)
    camera.setResolution(width, height)
    
    AprilTagBox = Apriltag.BoxDefination()
#
    input_stream = camera.getVideo()
    output_stream = CameraServer.putVideo('Processed', width, height)

    vision_nt = NetworkTables.getTable("Vision")

    img = np.zeros(shape=(480, 640, 3), dtype=np.uint8)

    while True:
        team_color = NetworkTables.getTable("team_color")
        start_time = time.time()

        frame_time, input_img = input_stream.grabFrame(img)
        output_img = np.copy(input_img) # copy the same img for processing

        if frame_time == 0:
            output_stream.notifyError(input_stream.getError())
            continue
        
        output_img = AprilTagBox.findTags(output_img)

        pocessing_time = time.time() - start_time
        fps = 1/pocessing_time
        cv.putText(output_img, str(round(fps, 1)), (0, 40),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        output_stream.putFrame(output_img)

        vision_nt.putNumber("TestFPS", fps)
        
if __name__ == '__main__': main()
