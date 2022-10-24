from cscore import CameraServer
from networktables import NetworkTables

import cv2 as cv
import numpy as np
import time

import Apriltag


def main():
    width = 640
    height = 480
    fps = 30
    mtx = np.array([[669.76134921, 0., 364.47532344],
                    [0., 669.8613114, 225.14641631],
                    [0., 0., 1.]])
    dist = np.array([[0.09899272, -0.34263704, 0.00170763,  0.01447023,  1.06025138]])
    cap = cv.VideoCapture(0)
    cap.set(5, fps)
    cap.set(3, width)
    cap.set(4, height)

    if not cap.isOpened():
        print("CAM error")
        exit()

    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
    output_img = np.copy(img)

    AprilTagBox = Apriltag.BoxDefination(mtx, dist)

    while True:
        start_time = time.time()
        ret, frame = cap.read()

        if not ret:
            break

        output_img = np.copy(frame)

        output_img = AprilTagBox.findTags(output_img)

        # print(output_img)

        pocessing_time = time.time() - start_time
        fps = 1/pocessing_time
        cv.putText(output_img, str(round(fps, 1)), (0, 40),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        cv.imshow("processing", output_img)

        if cv.waitKey(1) == ord('p'):
            cv.imwrite('./calibration.jpg', output_img)

        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


main()
