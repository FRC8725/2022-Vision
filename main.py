from cscore import CameraServer
from networktables import NetworkTables

import cv2 as cv
import numpy as np
import time

import Apriltag


def main():
    width = 1920
    height = 1080

    CameraServer.startAutomaticCapture(1)
    
    AprilTagBox = Apriltag.BoxDefination()
#
    input_stream = CameraServer.getVideo
    output_stream = CameraServer.putVideo('Processed', width, height)

    vision_nt = NetworkTables.getTable("Vision")

    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

    while True:
        start_time = time.time()

        frame_time, input_img = input_stream.grabFrame(img)
        output_img = np.copy(input_img) # copy the same img for processing

        if frame_time == 0:
            output_stream.notifyError(input_stream.getError())
            continue
        
        AprilTagBox.findTags(output_img)

        pocessing_time = time.time() - start_time
        fps = 1/pocessing_time
        cv.putText(output_img, str(round(fps, 1)), (0, 40),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        output_stream.putFrame(output_img)

        vision_nt.putNumber("TestFPS", fps)
        
main()
