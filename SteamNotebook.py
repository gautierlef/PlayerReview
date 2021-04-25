# %%
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def get_steam_site(username):
    return ''.join(['https://steamcommunity.com/id/', username, '/games/?tab=all'])


def get_hours(pseudo):
    wd_steam = webdriver.Chrome(executable_path="./chromedriver_win32/chromedriver.exe")
    wd_steam.get(get_steam_site(pseudo))
    games_list = wd_steam.find_elements_by_id("games_list_rows")
    if len(games_list) == 0:
        return None
    all_games = games_list[0].find_elements_by_class_name('gameListRow')
    game_stats = [game.text.split('Liens')[0] for game in all_games if 'heures' in game.text]
    game_stats = [game.strip() for game in game_stats]
    jeu = [game.split('\n')[0] for game in game_stats]
    heures = [game.split('\n')[1] for game in game_stats]
    heures = [float(heures.replace(',', '').split(' ')[0]) for heures in heures]
    player = {
        'name': pseudo,
        'games': dict(zip(jeu, heures))
    }
    return player


def jeux_communs(dic1, dic2):
    return [jeu for jeu in dic1["games"].keys() if jeu in dic2["games"].keys()]


def save_data(players):
    file = open("data.txt", "w",encoding='utf-8')
    content = ""
    for player in players:
        content += "Player|" + player["name"] + "\n"
        for game in player['games']:
            content += game + "|" + player["games"].get(game).__str__() + "\n"
    file.write(content)
    file.close()


def load_data():
    file = open('data.txt', 'r')
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


if __name__ == "__main__":
    players = load_data()
    pseudo = input("Entrer le pseudo du joueur :")
    found = False
    for player in players:
        if player['name'] == pseudo:
            found = True
            player = get_hours(pseudo)
            inputPlayer = player
            break
    if not found:
        inputPlayer = get_hours(pseudo)
        if inputPlayer is not None:
            players.append(inputPlayer)
    if inputPlayer is not None:
        for player in players:
            if player['name'] != pseudo:
                print("Jeux en commun avec :", player['name'], jeux_communs(inputPlayer, player))
        save_data(players)
    else:
        print("Le pseudo :", pseudo, "ne correspond à aucun compte.")
