#Import necessary libraries
from flask import request,Flask, render_template, Response
import cv2

#Initialize the Flask app
app = Flask(__name__)


def gen_frames(a,b,c):  
    print(a)
    print(b)
    print(c)
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream_feed')
def stream_feed():
    
    stream = request.args.get("stream")
    uname = request.args.get("uname")
    passw=request.args.get("passw")
    return Response(gen_frames(stream,uname,passw), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)