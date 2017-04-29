# main.py

from camera2 import VideoCamera
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, send, emit


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Yoko Shimomura is a Japanese composer and pianist, primarily known for her work in video games.'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on('connect')
def on_connect():
    emit('my response', {'data': 'Connected'})
    print("Server has connected to client")
    #print(data)

@socketio.on('disconnect', namespace='/test')
def on_disconnect():
    print('Client disconnected')
    
@socketio.on('message')
def on_message(msg):
    print('Message received: ' + msg)
    #send("Receieved " + msg['data'], broadcast=True)
    
    

if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True)
    socketio.run(app, host='0.0.0.0')