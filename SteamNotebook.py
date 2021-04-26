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
                        if game in recommendedGames:
                            for recommendedGame in recommendedGames["name"]:
                                if recommendedGame["name"] == game["name"]:
                                    game["nb"] += 1
                                    break
                            break
                        else:
                            recommendedGames.append({"name": game, "nb": 1})
                            break
    recommendedGames = sorted(recommendedGames, key=lambda k: k['nb'])
    print("\nVoici des jeux joués par des utilisateurs similaire à vous :")
    for i in range(0, 3):
        if recommendedGames[i] is not None:
            print(recommendedGames[i]['name'])


def recommend_players(players, inputPlayer):
    print('\nVous avez plusieurs jeux en commun avec ces joueurs peut être voudriez vous les contacter :')
    nbRecommendedPlayers = 0
    for player in players:
        if player != inputPlayer:
            nbCommonGame = 0
            commonGames = jeux_communs(inputPlayer, player)
            if len(commonGames) > 2:
                nbRecommendedPlayers += 1
                myStr = player['name'] + ' : '
                for game in player['games']:
                    if game in commonGames:
                        myStr += game + ', '
                        nbCommonGame += 1
                    if nbCommonGame > 2:
                        myStr = myStr[:-2]
                        print(myStr)
                        break
            if nbRecommendedPlayers > 2:
                break


if __name__ == '__main__':
    players = load_data()
    pseudo = input('Entrer le pseudo du joueur : ')
    inputPlayer = find_player(players, pseudo)
    if inputPlayer is not None:
        recommend_games(players, inputPlayer)
        recommend_players(players, inputPlayer)
        save_data(players)
    else:
        print('Le pseudo :', pseudo, 'ne correspond à aucun compte ou ce joueur n\'a pas de jeu.')
