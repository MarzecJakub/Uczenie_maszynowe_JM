import cv2
import numpy as np


#color ranges
lower_red_d = np.array([0,150,50])
upper_red_d = np.array([5,255,255])

lower_red = np.array([170,150,50])
upper_red = np.array([180,255,255])

#lower_blue = np.array([94,80,2])
#upper_blue = np.array([126,255,255])

lower_blue = np.array([100,160,30])
upper_blue = np.array([120,255,255])


kernel_o = np.ones((6,6),np.uint8)
kernel_c = np.ones((10,10),np.uint8)

cap = cv2.VideoCapture('one_round_cam.mp4')

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_test.mp4', fourcc, 50.0, (1920,1080), True)


fgbg = cv2.createBackgroundSubtractorMOG2()

while(cap.isOpened()):

    ret, frame = cap.read()

    if not ret:
        print("No more frames left.")
        break
        
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask1 = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_red1 = cv2.inRange(hsv, lower_red, upper_red)
    mask_red2 = cv2.inRange(hsv, lower_red_d, upper_red_d)
    fgmask = fgbg.apply(hsv)

    res = cv2.bitwise_and(frame, frame, mask = ((mask1|mask_red1|mask_red2)&fgmask))
    
    cleanedup_frame = cv2.morphologyEx(cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel_o), cv2.MORPH_CLOSE, kernel_c)
    
    out.write(cleanedup_frame)
    cv2.imshow('cleanedup_frame',cleanedup_frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
out.release()
print("Video saved successfully.")
cv2.destroyAllWindows() 