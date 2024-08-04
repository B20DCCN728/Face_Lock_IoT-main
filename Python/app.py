from flask import Flask, render_template, Response, jsonify
import Server_Camera
import cv2
import json

app = Flask(__name__)

def generate_camera_feed():
    while True:
        frame = Server_Camera.get_camera_frame()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/info')
def info():
    with open('last_name.json', 'r') as f:
        data = json.load(f)
        last_name = data['last_name']
    data = {
        "name": last_name
    }
    return jsonify(data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

