import os
from flask import Flask, send_from_directory, json
from flask_socketio import SocketIO
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__, static_folder='./build/static')

cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    json=json,
    manage_session=False
)

userList = []
specList = []

@app.route('/', defaults={"filename": "index.html"})
@app.route('/<path:filename>')
def index(filename):
    return send_from_directory('./build', filename)

@socketio.on('connect')
def on_connect():
    print('User connected!')

@socketio.on('disconnect')
def on_disconnect():
    print('User disconnected!')

@socketio.on('board')
def on_board(data):
    print(str(data))
    socketio.emit('board', data, broadcast=True, include_self=False)

@socketio.on('user')
def on_user(data):
    print(str(data))
    userList.append(data['username'])
    print(userList)
    if len(userList) == 1:
        socketio.emit('user', {'playerX': userList[0]}, broadcast=True, include_self=False)
    if len(userList) == 2:
        socketio.emit('user', {'playerX': userList[0], 'playerO': userList[1]}, broadcast=True, include_self=False)
    if len(userList) > 2:
        for i in range(2, len(userList)):
            if userList[i] not in specList:
                specList.append(userList[i])
        socketio.emit('user', {'playerX': userList[0], 'playerO': userList[1], 'spectators': specList}, broadcast=True, include_self=False)
    
    
if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
    )