import numpy as np
import cv2 as cv
from glob import glob
import json

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((6*9, 3), np.float32)
objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
# meshgrid -> transpose -> reshape(non-restriction, 2)

objpoints = []
imgpoints = []

imgs = glob('./imgs/*.jpg')

for fname in imgs:

    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(gray, (9, 6), None)
    print(ret)

    if ret == True:
        objpoints.append(objp)

        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (9, 6), corners2, ret)
        # cv.imshow('img', img)
        # cv.waitKey(500)

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None)

camera = {}


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


for variable in ['ret', 'mtx', 'dist', 'rvecs', 'tvecs']:
    camera[variable] = eval(variable)

with open('camera.json', 'w') as f:
    json.dump(camera, f, indent=4, cls=NumpyEncoder)

print(rvecs)
print(tvecs)
print(mtx, dist)
cv.destroyAllWindows()
img = cv.imread('./imgs/1666176498071798100.jpg')
h,  w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
# undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)
# crop the image
# x, y, w, h = roi
# dst = dst[y:y+h, x:x+w]
cv.imwrite('calibresult.png', dst)
