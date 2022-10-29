import pupil_apriltags as apriltag
import cv2 as cv
import numpy as np
from math import degrees, atan, sqrt

class BoxDefination():
    def __init__(self, mtx, dist):
        self.mtx = mtx
        self.camera_params = [mtx[0][0], mtx[1][1], mtx[0][2], mtx[1][2]]
        self.dectector = apriltag.Detector(families="tag36h11")
        self.dist = dist
        self.axis = np.float32(
            [[3, 0, 0], [0, 3, 0], [0, 0, -3]]).reshape(-1, 3)
        self.tag_size = 0.2

    def findTags(self, img, canva):
        imgc = np.copy(img)
        gray = cv.cvtColor(imgc, cv.COLOR_BGR2GRAY)
        tags = self.dectector.detect(gray, estimate_tag_pose=True, camera_params=self.camera_params, tag_size=0.2)
        if tags == None:
            return None
        
        data = []

        for tag in tags:

            objp = np.zeros((6*9, 3), np.float32)
            objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
            # meshgrid -> transpose -> reshape(non-restriction, 2)

            objpoints = []
            imgpoints = []

            (ptA, ptB, ptC, ptD) = tag.corners
            # print(tag.corners)
            ptA = (int(ptA[0]), int(ptA[1]))
            ptB = (int(ptB[0]), int(ptB[1]))
            ptC = (int(ptC[0]), int(ptC[1]))
            ptD = (int(ptD[0]), int(ptD[1]))

            cv.line(canva, ptA, ptB, (0, 255, 0), 2)
            cv.line(canva, ptB, ptC, (0, 255, 0), 2)
            cv.line(canva, ptC, ptD, (0, 255, 0), 2)
            cv.line(canva, ptD, ptA, (0, 255, 0), 2)

            center = (np.int32(tag.center[0]), np.int32(tag.center[1]))
            cv.circle(canva, center, 5, (0, 0, 255), -1)

            pose_R = tag.pose_R
            pose_t = tag.pose_t
            tagID = tag.tag_id
            # print(pose_R)
            # print("----------------------------")
            # print(pose_t)
            # print("----------------------------")

            corner = self.tag_size/2
            objPoints = np.array([[corner, 0, 0], [0, corner, 0], [0, 0, -corner], [0, 0, 0]])

            r11 = pose_R[0][0]
            r12 = pose_R[0][1]
            r13 = pose_R[0][2]
            r21 = pose_R[1][0]
            r22 = pose_R[1][1]
            r23 = pose_R[1][2]
            r31 = pose_R[2][0]
            r32 = pose_R[2][1]
            r33 = pose_R[2][2]

            AprilTagPitch = round(degrees(atan(-r31/sqrt((r32*r32)+(r33*r33)))), 3)
            AprilTagRoll = round(degrees(atan(-r32/r33)), 3)
            AprilTagYaw = round(degrees(atan(r21/r11)), 3)
            AprilTagX = pose_t[0][0]
            AprilTagY = pose_t[1][0]
            AprilTagZ = pose_t[2][0]
            
            rvec = [[r11, r12, r13],
                    [r21, r22, r23],
                    [r31, r32, r33]]
            rvec = np.array(rvec)
            # tvec = [[pose_R[3][0], pose_R[3][1], pose_R[3][2]]]
            tvec = [[AprilTagX, AprilTagY, AprilTagZ]]
            tvec = np.array(tvec)

            cv.putText(canva, f'{tagID}', center, cv.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 255))

            # print(AprilTagPitch)

            # imgpts = np.zeros((3, 2))

            imgpts, jac = cv.projectPoints(objPoints, rvec, tvec, self.mtx, self.dist)
            # print(imgpts)
            imgpts = np.array(imgpts, dtype=np.int32)
            img = self.draw(canva, center, imgpts)

            rX = self.convertData2Measurement(AprilTagX)
            rY = self.convertData2Measurement(AprilTagY)
            rZ = self.convertData2Measurement(AprilTagZ)

            # print(rX, rY, rZ)
            # print(AprilTagYaw, AprilTagPitch, AprilTagRoll)
            
            data.append([rX, rY, rZ, AprilTagPitch, AprilTagRoll, AprilTagYaw])
            
        return data

    def convertData2Measurement(self, data):
        return data/0.64*50

    def draw(self, img, center, imgpts):
        img = cv.line(img, center, tuple(imgpts[0].ravel()), (0, 0, 255), 2)
        img = cv.line(img, center, tuple(imgpts[1].ravel()), (0, 255, 0), 2)
        img = cv.line(img, center, tuple(imgpts[2].ravel()), (255, 0, 0), 2)
        return img

    def findBox(self, img):
        results = self.findTags(img)
        pass
    
    def findPosition(self, img):
        pass
    
