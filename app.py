"""app.py"""
import os
import random
from flask import Flask, send_from_directory, json
from flask_socketio import SocketIO
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
import models

load_dotenv(find_dotenv())

APP = Flask(__name__, static_folder='./build/static')

APP.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL')  #POINT TO HEROKU DATABASE

APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(APP)

DB.create_all()

CORS = CORS(APP, resources={r"/*": {"origins": "*"}})
SOCKETIO = SocketIO(APP,
                    cors_allowed_origins="*",
                    json=json,
                    manage_session=False)

USER_LIST = []
SPEC_LIST = []


@APP.route('/', defaults={"filename": "index.html"})
@APP.route('/<path:filename>')
def index(filename):
    """index"""
    return send_from_directory('./build', filename)


@SOCKETIO.on('connect')
def on_connect():
    """on_connect"""
    print('User connected!')


@SOCKETIO.on('disconnect')
def on_disconnect():
    """on_disconnect"""
    print('User disconnected!')


@SOCKETIO.on('board')
def on_board(data):
    """on_board"""
    print(str(data))
    SOCKETIO.emit('board', data)


@SOCKETIO.on('winner')
def on_winner(data):
    """on_winner"""
    # Disable all the no-member violations in this function
    # pylint: disable=no-member
    print(str(data))
    winner = DB.session.query(models.Person).get(data['winner'])
    loser = DB.session.query(models.Person).get(data['loser'])
    print(winner.score, loser.score)
    winner.score = winner.score + 1
    loser.score = loser.score - 1
    print(winner.score, loser.score)
    print("Updating Score")
    DB.session.commit()
    print("Score Updated!")
    all_users = models.Person.query.order_by(models.Person.score.desc()).all()
    users = []
    scores = []
    for player in all_users:
        users.append(player.username)
        scores.append(player.score)
    print(users)
    print(scores)
    SOCKETIO.emit('leaderboard', {'users': users, 'scores': scores})


@SOCKETIO.on('reset')
def on_reset(data):
    """on_reset"""
    print(str(data))
    SOCKETIO.emit('reset', {'message': 'Resetting Game'})


@SOCKETIO.on('user')  #{ username: userText }
def on_user(data):
    """on_user"""
    # Disable all the no-member violations in this function
    # pylint: disable=no-member
    print(str(data))
    exists = DB.session.query(DB.exists().where(
        models.Person.username == data['username'])).scalar()
    if not exists:
        print('Adding player on DB...')
        users, scores = add_user(data['user'])
        print(users)
        print(scores)
        SOCKETIO.emit('leaderboard', {'users': users, 'scores': scores})
    else:
        all_users = models.Person.query.order_by(
            models.Person.score.desc()).all()
        users = []
        scores = []
        for player in all_users:
            users.append(player.username)
            scores.append(player.score)
        print(users)
        print(scores)
        SOCKETIO.emit('leaderboard', {'users': users, 'scores': scores})

    add_user_to_list(data['username'])
    
    if len(USER_LIST) == 1:
        user_data = models.Person.query.filter_by(
            username=data['username']).first()
        SOCKETIO.emit(
            'playerX', {
                'playerX': USER_LIST[0],
                'username': data['username'],
                'score': user_data.score
            })
    elif len(USER_LIST) == 2:
        user_data = models.Person.query.filter_by(
            username=data['username']).first()
        SOCKETIO.emit(
            'playerO', {
                'playerO': USER_LIST[1],
                'username': data['username'],
                'score': user_data.score
            })
    else:
        for i in range(2, len(USER_LIST)):
            if USER_LIST[i] not in SPEC_LIST:
                SPEC_LIST.append(USER_LIST[i])
        print("Spect: " + str(SPEC_LIST))
        SOCKETIO.emit('spectators', {'spectators': SPEC_LIST})

def add_user_to_list(username):
    if username not in USER_LIST:
        USER_LIST.append(username)
    return USER_LIST
        
def add_user(username):
    rand = random.randint(0, 500)
    new_user = models.Person(id=rand, username=username, score=100)
    DB.session.add(new_user)
    DB.session.commit()
    all_users = models.Person.query.all()
    users = []
    scores = []
    for player in all_users:
        users.append(player.username)
        scores.append(player.score)
    return users, scores

if __name__ == "__main__":
    SOCKETIO.run(
        APP,
        host=os.getenv('IP', '0.0.0.0'),
        port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
    )
