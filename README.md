# Project 2

Ian Gabrielle Gojo Cruz  
CS 490 - 004  

## Description  

This project is for CS 490 class at NJIT.  
This is a simple _Tic Tac Toe_ webapp that utilize [React](https://reactjs.org/docs/getting-started.html) and [SocketIO](https://socket.io/docs/v3/index.html).  

## Language and Libraries  
1. Python
2. Flask
3. HTML
4. CSS
5. Heroku
6. React
7. SocketIO
 
## Installation  

1. `npm install`
2. `pip install -r requirements.txt`
3. `npm install -g heroku`
4. `npm install -U flask-cors`
5. `npm install socket.io-client --save`
6. `npm install -U flask`

## Known Problems and Solutions  
### 1. Multiple emits received on several clients.  

I separated each socket.on on different useEffect()

### 2. Alternating X and O. 

I had to write conditional statements checking if xNext is true and if username == Player X and vice versa for Player O.

### 3. Specatators.  

Appending the last element instead of  resetting the spectList worked for me.

# WIP  
