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

wd_steam.get(get_steam_site('bullshit'))


#%%
games_list = wd_steam.find_elements_by_id("games_list_rows")
games_tab = games_list[0]
all_games = games_tab.find_elements_by_class_name('gameListRow')


#%%

game_stats = [game.text.split('Liens')[0] for game in all_games if 'heures' in game.text]
game_stats = [game.strip() for game in game_stats]

#%%

jeu = [game.split('\n')[0] for game in game_stats]
heures = [game.split('\n')[1] for game in game_stats]
heures = [float(heures.split(' ')[0]) for heures in heures]

dic_jeu_heure = dict(zip(jeu,heures))
#%%

stats_presentes = [game for game in all_games if 'stats' in game.text]

#%%
#stats_controls = [stats_presentes[i].find_elements_by_class_name('bottom_controls') for i in range(len(stats_presentes))]
#%%