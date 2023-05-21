import cv2
 
capture0 = cv2.VideoCapture(0)
capture1 = cv2.VideoCapture(1)
 
# fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
# videoWriter = cv2.VideoWriter('video.avi', fourcc, 30.0, (640,480))
 
while (True):
 
    ret0, frame0 = capture0.read()
    ret1, frame1 = capture1.read()
     
    if ret0:
        cv2.imshow('video0', frame0)
    if ret1:
        cv2.imshow('video1', frame1)
        # videoWriter.write(frame)
 
    if cv2.waitKey(1) == 27:
        break
 
capture0.release()
capture1.release()
# videoWriter.release()
 
cv2.destroyAllWindows()