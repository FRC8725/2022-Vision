import cv2 as cv
import numpy as np
import time

def main():
    width = 1920/4
    height = 1080/4
    fps = 30
    
    cap = cv.VideoCapture(0) 
    cap.set(5, fps)
    cap.set(3, width)
    cap.set(4, height)
    
    if not cap.isOpened():
        print("CAM error")
        exit()

    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
    output_img = np.copy(img)

    while True:
        start_time = time.time()
        ret, frame = cap.read()
        
        if not ret:
            break
        
        output_img = np.copy(frame)
        

        pocessing_time = time.time() - start_time
        fps = 1/pocessing_time
        cv.putText(output_img, str(round(fps, 1)), (0, 40),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        cv.imshow("processing", output_img)
        
        if cv.waitKey(1) == ord('q'):
            break
        
    cap.release()
    cv.destroyAllWindows()

main()