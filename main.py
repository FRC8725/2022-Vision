from cscore import CameraServer, UsbCamera
# from networktables import NetworkTables
from networktables import NetworkTablesInstance

import cv2 as cv
import numpy as np
import time
import json
import sys

import calTags
import BallDetection as BDetect

configFile = "/boot/frc.json"

team = None
server = False
cameraConfigs = []
switchedCameraConfigs = []
cameras = []

def parseError(str):
    """Report parse error."""
    print("config error in '" + configFile + "': " + str, file=sys.stderr)
    
def readConfig():
    """Read configuration file."""
    global team
    global server

    # parse file
    try:
        with open(configFile, "rt", encoding="utf-8") as f:
            j = json.load(f)
    except OSError as err:
        print("could not open '{}': {}".format(configFile, err), file=sys.stderr)
        return False

    # top level must be an object
    if not isinstance(j, dict):
        parseError("must be JSON object")
        return False

    # team number
    try:
        team = j["team"]
    except KeyError:
        parseError("could not read team number")
        return False

    # ntmode (optional)
    if "ntmode" in j:
        str = j["ntmode"]
        if str.lower() == "client":
            server = False
        elif str.lower() == "server":
            server = True
        else:
            parseError("could not understand ntmode value '{}'".format(str))

    # # cameras
    # try:
    #     cameras = j["cameras"]
    # except KeyError:
    #     parseError("could not read cameras")
    #     return False
    # for camera in cameras:
    #     if not readCameraConfig(camera):
    #         return False

    # # switched cameras
    # if "switched cameras" in j:
    #     for camera in j["switched cameras"]:
    #         if not readSwitchedCameraConfig(camera):
    #             return False

    return True

def scaleCameraMtx(widthA, widthB, mtx):
    scale = widthB / widthA
    mtx[0][0] *= scale
    mtx[1][1] *= scale
    mtx[0][2] *= scale
    mtx[1][2] *= scale
    
class CameraConfig: pass

def main():
    global configFile
    
    with open('camera.json', 'r') as jsonfile:
        camera_data = json.load(jsonfile)
        
    with open(configFile, 'r') as j:
        config = json.load(j)

    widthbase = camera_data['width']
    heightbase = camera_data['height']
    fpsbase = camera_data['fps']
    mtx = np.array(camera_data['mtx'])
    dist = np.array(camera_data['dist'])
    
    cam_configs = config['cameras']
    for camcfg in cam_configs:
        cam = CameraConfig()
        cam.name = camcfg['name']
        cam.path = camcfg['path']
        cam.width = camcfg['width']
        cam.height = camcfg['height']
        cam.fps = camcfg['fps']
        cameras.append(cam)
    
    width = cameras[0].width
    height = cameras[0].height
    fps = cameras[0].fps
    # width = camera_data['width']
    # height = camera_data['height']
    
    print(mtx)
    scaleCameraMtx(widthbase, width, mtx)
    print("---")
    print(mtx)
    CameraServer.enableLogging()

    inst = CameraServer.getInstance()
    camera = UsbCamera(name=cameras[0].name, path=cameras[0].path)
    inst.startAutomaticCapture(camera=camera)
    
    AprilTagBox = calTags.AprilTagsDefination(mtx, dist)
#
    input_stream = inst.getVideo()
    output_stream = inst.putVideo('Processed', width, height)

    # vision_nt = NetworkTables.getTable("Vision")

    img = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    output_img = np.copy(img)
    
    if len(sys.argv) >= 2:
        configFile = sys.argv[1]

    # read configuration
    if not readConfig():
        sys.exit(1)
    
    ntinst = NetworkTablesInstance.getDefault()
    if server:
        print("Setting up NetworkTables server")
        ntinst.startServer()
    else:
        print("Setting up NetworkTables client for team {}".format(team))
        ntinst.startClientTeam(team)
        ntinst.startDSClient()

    vision_nt = ntinst.getTable('Vision')
    
    while True:
        # team_color = NetworkTables.getTable("team_color")
        start_time = time.time()

        frame_time, frame = input_stream.grabFrame(img)
        output_img = np.copy(frame) # copy the same img for processing
        

        if frame_time == 0:
            output_stream.notifyError(input_stream.getError())
            continue
        
        AprilTagBox.findTags(frame, output_img)
        BDetect.BallDetection(frame, output_img, '');

        pocessing_time = time.time() - start_time
        fps = 1/pocessing_time
        cv.putText(output_img, str(round(fps, 1)), (0, 40),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    
        output_stream.putFrame(output_img)
        # cv.imshow('ttt', frame)
        vision_nt.putNumber("TestFPS", fps)
        
if __name__ == '__main__': 
    main()
    