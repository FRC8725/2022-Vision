import cv2 as cv
import numpy as np
import time

width = 640
height = 480
fps = 30

cap = cv.VideoCapture(0)
cap.set(5, fps)
cap.set(3, width)
cap.set(4, height)

while True:
    start_time = time.time_ns()
    print(f'\r{start_time}')
    ret, frame = cap.read()
    cv.imshow('test', frame)

    if not ret:
        break
    if cv.waitKey(1) == ord('p'):
        cv.imwrite(f'./imgs/{start_time}.jpg', frame)

    if cv.waitKey(1) == ord('q'):
        break

cv.destroyAllWindows()
