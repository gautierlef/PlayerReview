from flask import Flask, render_template, request

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def accueil():
    return render_template('vueAccueil.html')


@app.route('/recherche', methods=['GET'])
def recherche():
    return render_template('vueRecherche.html')


@app.route('/joueur', methods=['POST'])
def rechercheJoueur():
    pseudo = request.form['pseudo']
    players = load_data()
    inputPlayer = find_player(players, pseudo)
    if inputPlayer is not None:
        recommendedGames = recommend_games(players, inputPlayer)
        recommendedPlayers = recommend_players(players, inputPlayer)
        save_data(players)
    else:
        return render_template('vueErreur.html', pseudo=pseudo)
    if len(recommendedGames) == 0 or len(recommendedPlayers) == 0:
        return render_template('vueManque.html', pseudo=pseudo)
    return render_template('vueJoueur.html', pseudo=pseudo, recommendedGames=recommendedGames, recommendedPlayers=recommendedPlayers)


def get_steam_site(username):
    return ''.join(['https://steamcommunity.com/id/', username, '/games/?tab=all'])


def get_hours(pseudo):
    wd_steam = webdriver.Chrome(executable_path="./chromedriver_win32/chromedriver.exe")
    wd_steam.get(get_steam_site(pseudo))
    games_list = wd_steam.find_elements_by_id("games_list_rows")
    if len(games_list) == 0:
        return None
    all_games = games_list[0].find_elements_by_class_name('gameListRow')
    if len(all_games) == 0:
        return None
    game_stats = [game.text.split('Liens')[0] for game in all_games if 'heures' in game.text]
    game_stats = [game.strip() for game in game_stats]
    jeu = [game.split('\n')[0] for game in game_stats]
    heures = [game.split('\n')[1] for game in game_stats]
    heures = [float(heures.replace(',', '').split(' ')[0]) for heures in heures]
    player = {
        'name': pseudo,
        'games': dict(zip(jeu, heures))
    }
    wd_steam.close()
    return player


def jeux_communs(dic1, dic2):
    return [jeu for jeu in dic1["games"].keys() if jeu in dic2["games"].keys()]


def save_data(players):
    file = open("data.txt", "w", encoding='utf-8')
    content = ""
    for player in players:
        content += "Player|" + player["name"] + "\n"
        for game in player['games']:
            content += game + "|" + player["games"].get(game).__str__() + "\n"
    file.write(content)
    file.close()


def load_data():
    file = open('data.txt', 'r', encoding='utf-8')
    players = []
    data = file.read().splitlines()
    for line in data:
        left = line.split('|')[0]
        right = line.split('|')[1]
        if left == 'Player':
            player = {
                'name': right,
                'games': {}
            }
            players.append(player)
        else:
            player['games'][left] = float(right)
    return players


def find_player(players, pseudo):
    index = 0
    for player in players:
        if player['name'] == pseudo:
            player = get_hours(pseudo)
            players[index] = player
            return player
        index += 1
    return add_new_player(players, pseudo)


def add_new_player(players, pseudo):
    newPlayer = get_hours(pseudo)
    players.append(newPlayer)
    return newPlayer


def recommend_games(players, inputPlayer):
    recommendedGames = []
    for player in players:
        if player != inputPlayer:
            commonGames = jeux_communs(inputPlayer, player)
            if len(commonGames) > 10:
                for game in player['games']:
                    if game not in commonGames:
                        gameAlreadyRecommended = False
                        for recommendedGame in recommendedGames:
                            if recommendedGame["name"] == game:
                                recommendedGame["nb"] += 1
                                gameAlreadyRecommended = True
                                break
                        if not gameAlreadyRecommended:
                            recommendedGames.append({"name": game, "nb": 1})
                        break
    recommendedGames = sorted(recommendedGames, key=lambda k: k['nb'])
    recommendedGames.reverse()
    recommendedGames = recommendedGames[:3]
    return recommendedGames


def recommend_players(players, inputPlayer):
    nbRecommendedPlayers = 0
    recommendedPlayers = []
    for player in players:
        if player != inputPlayer:
            nbCommonGame = 0
            commonGames = jeux_communs(inputPlayer, player)
            if len(commonGames) > 2:
                nbRecommendedPlayers += 1
                recommendedPlayer = {'name': player['name'], 'games': []}
                for game in player['games']:
                    if game in commonGames:
                        recommendedPlayer['games'].append(game)
                        nbCommonGame += 1
                    if nbCommonGame > 2:
                        recommendedPlayers.append(recommendedPlayer)
                        break
            if nbRecommendedPlayers > 2:
                break
    return recommendedPlayers


if __name__ == '__main__':
    app.run()
