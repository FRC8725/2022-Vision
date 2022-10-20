import pupil_apriltags as apriltag
import cv2 as cv
import numpy as np 

class BoxDefination():
    def __init__(self, mtx, dist):
        self.mtx = mtx
        self.camera_params = [mtx[0][0], mtx[1][1], mtx[0][2], mtx[1][2]]
        self.dectector = apriltag.Detector(families="tag36h11")
        self.dist = dist
        self.axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
    
    def findTags(self, img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        tags = self.dectector.detect(gray, estimate_tag_pose=True, camera_params=self.camera_params, tag_size=0.2)
        if tags == None: return img 
        print(tags)
        
        for tag in tags:
            (ptA, ptB, ptC, ptD) = tag.corners
            ptA = (int(ptA[0]), int(ptA[1]))
            ptB = (int(ptB[0]), int(ptB[1]))
            ptC = (int(ptC[0]), int(ptC[1]))
            ptD = (int(ptD[0]), int(ptD[1]))
            
            cv.line(img, ptA, ptB, (0, 255, 0), 2)
            cv.line(img, ptB, ptC, (0, 255, 0), 2)
            cv.line(img, ptC, ptD, (0, 255, 0), 2)
            cv.line(img, ptD, ptA, (0, 255, 0), 2)
            
            center = (np.int32(tag.center[0]), np.int32(tag.center[1]))
            cv.circle(img, center, 5, (0, 0, 255), -1)
            
            pose_R = tag.pose_R
            pose_t = tag.pose_t
            tagID = tag.tag_id
            
            cv.putText(img, f'{tagID}', center , cv.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 255))
            print(tagID)
            
            # imgpts = np.zeros((3, 2))
            
            # center = (cx, cy)
            # imgpts, jac = cv.projectPoints(self.axis, pose_R, pose_t, self.mtx, self.dist)
            # print(imgpts[0].ravel())
            # img = cv.line(img, center, tuple(imgpts[0].ravel()), (0,255,0), 5)
            # img = cv.line(img, center, tuple(imgpts[1].ravel()), (0,255,0), 5)
            # img = cv.line(img, center, tuple(imgpts[2].ravel()), (0,0,255), 5)
            
        return img
            
    def findBox(self, img):
        results = self.detector.detect(img)
        pass