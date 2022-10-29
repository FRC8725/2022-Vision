import cv2 as cv
import numpy as np
import time
import json

with open('camera.json', 'r') as jsonfile:
    camera_data = json.load(jsonfile)

width = camera_data['width']
height = camera_data['height']
fps = camera_data['fps']

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
