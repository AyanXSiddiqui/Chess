from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Initial game state
game_state = {
    'board': [['' for _ in range(5)] for _ in range(5)],
    'players': ['player1', 'player2'],
    'current_turn': 'player1',
    'game_over': False
}

def check_winner(board):
    # Add logic to check for winner if necessary
    pass

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    print('Client connected')
    emit('game_state', game_state)

@socketio.on('move')
def on_move(data):
    row, col, player = data['row'], data['col'], data['player']
    if game_state['current_turn'] == player and game_state['board'][row][col] == '':
        game_state['board'][row][col] = player  # Mark the board
        game_state['current_turn'] = 'player2' if player == 'player1' else 'player1'
        check_winner(game_state['board'])
        emit('game_state', game_state, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
