import cv2
# defining face detector
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
ds_factor=0.6
class VideoCamera(object):
    def __init__(self):
       #capturing video
       self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        #releasing camera
        self.video.release()

    def get_frame(self):
       #extracting frames
        ret, frame = self.video.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        face_rects=face_cascade.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in face_rects:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            break
        # # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def click_frame(self):
           #extracting frames
        ret, frame = self.video.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  
        ret, gray = cv2.imencode('.jpg', gray)
        ret, frame = cv2.imencode('.jpg', frame)
        return [frame.tobytes(),gray.tobytes()]
    

    