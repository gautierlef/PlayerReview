#%%
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
#%%

IS_LINUX = False

# In[3]:

def get_steam_site(username):
    return ''.join(['https://steamcommunity.com/id/',username,'/games/?tab=all'])

def get_lol_site(username):
    return ''.join(['https://euw.op.gg/summoner/userName=',username])

def get_wol_site(country,username):
    return ''.join(['https://wol.gg/stats/',country,'/',username])

#%%

chrome = webdriver.Chrome(executable_path="./chromedriver_win32/chromedriver.exe" if not IS_LINUX else "./chromedriver_linux")

#%%

chrome.get(get_steam_site('bullshit'))


#%%
games_list = chrome.find_elements_by_id("games_list_rows")
games_tab = games_list[0]
all_games = games_tab.find_elements_by_class_name('gameListRow')


#%%

game_stats = [game.text.split('Liens')[0] for game in all_games if 'heures' in game.text]
game_stats = [game.strip() for game in game_stats]

#%%

stats_presentes = [game for game in all_games if 'stats' in game.text]

#%%

controls = stats_presentes[0].find_elements_by_class_name('bottom_controls')
#%%

controls[0].click()
#%%
stats_presentes[0].text

#%%
link = chrome.find_element_by_class_name('pullup_item')

#%%:


class HttpRequest:
    def __init__(self):
        self.ua = "User agent"

    def get_url(self, url, timeout=10, retry=4):
        if retry < 1:
            return None
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
        }
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code != 200:
                raise requests.exceptions.BaseHTTPError
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.ConnectTimeout:
            print("Timeout")
            self.get_url(url, timeout=timeout + 1, retry=retry - 1)
        except requests.exceptions.BaseHTTPError:
            print("Erreur")
            self.get_url(url, timeout=timeout, retry=retry - 1)


# In[3]:


liste_sites = ['https://euw.op.gg/summoner/userName=','https://wol.gg/stats/euw/','https://steamcommunity.com/id/USERNAME/games/?tab=all']


# In[4]:


pseudo = input('Entrer le pseudo que vous rechercher :')


#%%


soup = HttpRequest().get_url(get_steam_site('bullshit'))


#%%


chrome.get(get_lol_site('arakniro'))


#%%


rank = chrome.find_element_by_class_name("LadderRank")


#%%


rang = rank.text.split(' ')


#%%


rank.text.split(' ')[2]


#%%


win_ratio = chrome.find_element_by_class_name('WinRatioTitle')


#%%


nb_parties,nb_victoires,nb_defaites = win_ratio.text.split(' ').join([i for i in win_ratio.text if i.isdigit()])


#%%


nb_parties,nb_victoires,nb_defaites


#%%


''.join([i for i in win_ratio.text if i.isdigit()])


# In[ ]:




