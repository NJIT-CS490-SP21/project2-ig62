import os
from flask import Flask, send_from_directory, json
from flask_socketio import SocketIO
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__, static_folder='./build/static')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') #POINT TO HEROKU DATABASE

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Person
db.create_all()

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
    socketio.emit('board', data, broadcast=True, include_self=True)

@socketio.on('reset')
def on_reset(data):
    socketio.emit('reset', {'message': 'Resetting Game'}, broadcast=True, include_self=True)

@socketio.on('user')
def on_user(data):
    print(str(data))
    if data['username'] not in userList:
        userList.append(data['username'])
    if len(userList) == 1:
        socketio.emit('playerX', {'playerX': userList[0], 'username': data['username']}, broadcast=True, include_self=True)
    elif len(userList) == 2:
        socketio.emit('playerO', {'playerO': userList[1], 'username': data['username']}, broadcast=True, include_self=True)
    else:
        for i in range(2, len(userList)):
            if userList[i] not in specList:
                specList.append(userList[i])
        print("Spect: " + str(specList))
        socketio.emit('spectators', {'spectators': specList}, broadcast=True, include_self=True)
    
    
if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
    )