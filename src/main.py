from flask import Flask, render_template, Response
from camera import VideoCamera
import numpy as np
import face_recognition as fr
import cv2
app = Flask(__name__)
@app.route('/')
def index():
    # rendering webpage
    return render_template('face.html')
def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield(b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def capture():
    video = cv2.VideoCapture(0)
    face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    ret, frame = video.read()
    face_rects=face_cascade.detectMultiScale(frame,1.3,5)

    my_image = fr.load_image_file("2.jpg")
    my_face_encoding = fr.face_encodings(my_image)[0]

    known_face_encondings = [my_face_encoding]
    known_face_names = ["SD"]       

    rgb_frame = frame[:, :, ::-1]

    face_locations = fr.face_locations(rgb_frame)
    face_encodings = fr.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        matches = fr.compare_faces(known_face_encondings, face_encoding)

        name = "Unknown"

        face_distances = fr.face_distance(known_face_encondings, face_encoding)

        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            return True
    
        
    return False





@app.route('/get_p')
def click():
    res=capture()
    if res==True:
        return render_template('shop.html')
    else:
        return 'No'


if __name__ == '__main__':
    app.run(debug=True)