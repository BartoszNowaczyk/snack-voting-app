from flask import Flask, render_template, request, redirect, url_for
import random
import json
from datetime import datetime
import redis

# Konfiguracja połączenia z Redis (zmiana hosta na 'redis')
r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

app = Flask(__name__)

# Lista 16 nazw przekąsek
snack_names = [
    "Chipsy ziemniaczane", "Czekolada", "Orzeszki", "Ciastka", "Popcorn", "Krakersy",
    "Praliny", "Żelki", "Lody", "Ciasteczka owsiane", "Lizaki", "Rogaliki",
    "Pianki", "Pączek", "Rurka z kremem", "Paszteciki"
]

# Lista odpowiadających nazwom zdjęć
snack_images = [
    "chipsy_ziemniaczane.jpg", "czekolada.jpg", "orzeszki.jpg", "ciastka.jpg", "popcorn.jpg",
    "krakersy.jpg", "praliny.jpg", "zelki.jpg", "lody.jpg", "ciasteczka_owsiane.jpg", "lizaki.jpg",
    "rogaliki.jpg", "pianki.jpg", "pączek.jpg", "rurkazkremem.jpg", "paszteciki.jpg"
]

# Inicjalizacja zawodników
initial_players = [{"name": snack, "id": i + 1, "image": snack_images[i]} for i, snack in enumerate(snack_names)]
players = initial_players.copy()
round_winners = []
current_round = []
round_number = 1

# Funkcja do wczytywania historii zwycięzców z Redis
def load_history():
    history = r.get('history')
    if history:
        return json.loads(history)
    else:
        return []

# Funkcja do zapisywania historii zwycięzców do Redis
def save_winner(winner_name):
    history = load_history()
    history.append({"winner": winner_name, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
    r.set('history', json.dumps(history))

@app.route('/')
def index():
    global players, current_round, round_winners, round_number

    # Wczytaj historię z Redis
    history = load_history()

    if len(players) == 1:
        winner = players[0]
        winner_image = winner['image']
        save_winner(winner['name'])  # Zapisujemy zwycięzcę
        return render_template('index.html', winner=winner['name'], winner_image=winner_image, history=history)

    if not current_round:
        random.shuffle(players)
        current_round = [(players[i], players[i + 1]) for i in range(0, len(players), 2)]

    current_match = current_round[0]

    return render_template('index.html', match=current_match, round_number=round_number, history=history)

@app.route('/vote', methods=['POST'])
def vote():
    global players, current_round, round_winners, round_number
    
    winner_id = int(request.form['winner'])
    winner = next(p for p in [current_round[0][0], current_round[0][1]] if p['id'] == winner_id)
    
    round_winners.append(winner)
    current_round.pop(0)

    if len(current_round) == 0:
        players = round_winners
        round_winners = []
        current_round = []
        round_number += 1

    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    global players, round_winners, current_round, round_number
    players = initial_players.copy()
    round_winners = []
    current_round = []
    round_number = 1
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
