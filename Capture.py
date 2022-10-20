import cv2 as cv
import numpy as np
import time

cap = cv.VideoCapture(0)

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
