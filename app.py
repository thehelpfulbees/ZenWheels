# main.py

#imports for bluetooth
from bluetooth_for_server import MainWindow
import sys
import thread
from bluetooth import *
import binascii
from PyQt4.QtGui import QApplication, QMainWindow
from PyQt4 import QtCore
from ui_Car import Ui_MainWindow

#imports for flask
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, send, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'butts'

#bluetooth_app = None
#window = None
bluetooth_app = QApplication(sys.argv)
window = MainWindow()
window.show()

socketio = SocketIO(app)
keys = [False]*200

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def on_connect():
    emit('echo', {'data': 'Connected'})
    print("Server has connected to client")
    #print(data)

@socketio.on('disconnect', namespace='/test')
def on_disconnect():
    print('Client disconnected')
    
@socketio.on('message')
def on_message(msg):
    print('Message received: ' + msg)
    emit('echo', {'data': "Server received message: "+str(msg)})

@socketio.on('carconnect')
def on_carconnect(data):
    emit('echo', {'data': "Now scanning for nearby cars"})
    window.tryToConnect()
    
@socketio.on('keydown')
def on_keydown(data):
    keycode = data[u'id']
    keys[keycode] = True;
    emit('echo', {'data': "Keydown: "+str(keycode)})

    window.keyPress(keycode)

@socketio.on('keyup')
def on_keyup(data):
    keycode = data[u'id']
    keys[keycode] = False;
    emit('echo', {'data': "Keyup: "+str(keycode)})

def main():
    
    #app.run(host='0.0.0.0', debug=True)
    socketio.run(app, host='127.0.0.1')
    #sys.exit(bluetooth_app.exec_())
    
if __name__ == '__main__':
    main()
