#%%
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

#%%

def get_steam_site(username):
    return ''.join(['https://steamcommunity.com/id/',username,'/games/?tab=all'])


#%%

wd_steam = webdriver.Chrome(executable_path="./chromedriver_win32/chromedriver.exe" )

#%%


#%%

def get_hours(pseudo):
    wd_steam.get(get_steam_site(pseudo))
    games_list = wd_steam.find_elements_by_id("games_list_rows")
    all_games = games_list[0].find_elements_by_class_name('gameListRow')
    game_stats = [game.text.split('Liens')[0] for game in all_games if 'heures' in game.text]
    game_stats = [game.strip() for game in game_stats]
    jeu = [game.split('\n')[0] for game in game_stats]
    heures = [game.split('\n')[1] for game in game_stats]
    heures = [float(heures.replace(',','').split(' ')[0]) for heures in heures]
    return dict(zip(jeu,heures))

#%%

dic_vol = get_hours('vol')
dic_bs = get_hours('bullshit')

#%%

def jeux_communs(dic1,dic2):
    return [jeu for jeu in dic1.keys() if jeu in dic2.keys()]

#%%
#stats_controls = [stats_presentes[i].find_elements_by_class_name('bottom_controls') for i in range(len(stats_presentes))]
#%%