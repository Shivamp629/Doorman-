from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, disconnect
from socket import *
import sys, os, time, json, hashlib, base64
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)
cvSocket = None

trueEmotion = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('my event', namespace='/test')
def my_event(msg):
    print(msg['data'])

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

def changeSong(message):
    emotion = message.decode()
    print(emotion)

    global trueEmotion
    if (trueEmotion == emotion):
        return

    trueEmotion = emotion

    if emotion == 'happy':
        song = 'y6Sxv-sUYtM'
    elif emotion == 'sad':
        song = '8Wl-HSl386k'
    elif emotion == 'angry':
        song = 'Zv479MCnThA'
    elif emotion == 'disgust':
        song = 'yzTuBuRdAyA'
    elif emotion == 'fear':
        song = '4V90AmXnguw'
    elif emotion == 'surprise':
        song = 'xTlNMmZKwpA'
    elif emotion == 'neutral':
        song = 'ymHBUyui_ws'
    else:
        song = 'ymHBUyui_ws'

    socketio.emit('message', {'emotion': emotion, 'song': song}, namespace='/test')


def startCVSocket():
    global cvSocket
    cvSocket = socket(AF_INET, SOCK_DGRAM)
    cvSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    cvSocket.bind(("127.0.0.1", 8003))
    while True:
        message, clientAddress = cvSocket.recvfrom(2048)
        changeSong(message)

if __name__ == '__main__':
    try:
        Thread(target=startCVSocket).start()
        socketio.run(app)
    except KeyboardInterrupt:
        cvSocket.close()
        os._exit(1)
