import os
import random
from flask import Flask, send_from_directory, json
from flask_socketio import SocketIO
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__, static_folder='./build/static')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') #POINT TO HEROKU DATABASE

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

import models
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
    socketio.emit('board', data)
    
@socketio.on('game_status')
def on_game_status(data):
    print(str(data))
    socketio.emit('get_winner', data)

@socketio.on('winner')
def on_winner(data):
    print(str(data))
    winner = db.session.query(models.Person).get(data['winner'])
    loser = db.session.query(models.Person).get(data['loser'])
    print(winner.score, loser.score)
    winner.score = winner.score + 1
    loser.score = loser.score - 1
    print(winner.score, loser.score)
    print("Updating Score")
    db.session.commit()
    print("Score Updated!")
    all_users = models.Person.query.order_by(models.Person.score.desc()).all()
    users = []
    scores = []
    for player in all_users:
        users.append(player.username)
        scores.append(player.score)
    print(users)
    print(scores)
    socketio.emit('leaderboard', {'users': users, 'scores': scores})

@socketio.on('reset')
def on_reset(data):
    socketio.emit('reset', {'message': 'Resetting Game'})

@socketio.on('user') #{ username: userText }
def on_user(data):
    print(str(data))
    exists = db.session.query(db.exists().where(models.Person.username == data['username'])).scalar()
    if not exists:
        print('Adding player on db...')
        rand = random.randint(0, 500)
        new_user = models.Person(id=rand,username=data['username'], score = 100)
        db.session.add(new_user)
        db.session.commit()
        all_users = models.Person.query.order_by(models.Person.score.desc()).all()
        users = []
        scores = []
        for player in all_users:
            users.append(player.username)
            scores.append(player.score)
        print(users)
        print(scores)
        socketio.emit('leaderboard', {'users': users, 'scores': scores})
    else:
        # user_data = db.session.query(models.Person).get(data['username'])
        # username = user_data.username
        # score = user_data.score
        all_users = models.Person.query.order_by(models.Person.score.desc()).all()
        users = []
        scores = []
        for player in all_users:
            users.append(player.username)
            scores.append(player.score)
        print(users)
        print(scores)
        socketio.emit('leaderboard', {'users': users, 'scores': scores})
        
    if data['username'] not in userList:
        userList.append(data['username'])
    if len(userList) == 1:
        user_data = models.Person.query.filter_by(username=data['username']).first()
        socketio.emit('playerX', {'playerX': userList[0], 'username': data['username'], 'score':user_data.score})
    elif len(userList) == 2:
        user_data = models.Person.query.filter_by(username=data['username']).first()
        socketio.emit('playerO', {'playerO': userList[1], 'username': data['username'], 'score':user_data.score})
    else:
        for i in range(2, len(userList)):
            if userList[i] not in specList:
                specList.append(userList[i])
        print("Spect: " + str(specList))
        socketio.emit('spectators', {'spectators': specList})
    
    
if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
    )