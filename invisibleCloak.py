import cv2
import numpy as np

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

imgTarget=cv2.imread("resources/hall_target4.jpg")
hT,wT,cT=imgTarget.shape
cap=cv2.VideoCapture(0)
cap.set(3,wT)
cap.set(4,hT)
cap.set(10,100)
#[h_min,h_max,s_min,s_max,v_min,v_max]
color_matrix=[[85,145,125,255,0,255]]
k=0

while True:
    success,imgWebcam=cap.read()
    imgHSV=cv2.cvtColor(imgWebcam,cv2.COLOR_BGR2HSV)
    lower = np.array([color_matrix[k][0], color_matrix[k][2], color_matrix[k][4]]) #100,129,129,247,24,237
    upper = np.array([color_matrix[k][1], color_matrix[k][3], color_matrix[k][5]])
    mask = cv2.inRange(imgHSV, lower, upper)
    maskInv=cv2.bitwise_not(mask)
    imgTargetNeeded=cv2.bitwise_and(imgTarget,imgTarget,mask=mask)
    imgWN=cv2.bitwise_and(imgWebcam,imgWebcam,mask=maskInv)
    imgResult=cv2.bitwise_or(imgTargetNeeded,imgWN)
    # imgStack=stackImages(0.25,([imgWebcam,imgTarget],[mask,maskInv],[imgTargetNeeded,imgWN],[imgWebcam,imgResult]))
    # cv2.imshow("Flow",imgStack)
    cv2.imshow("Result",imgResult)
    cv2.waitKey(1)