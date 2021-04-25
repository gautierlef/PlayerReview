import requests
import re
from bs4 import BeautifulSoup


class HttpRequest:
    """ Creates an HttpRequest of a specific URL request """
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


# https://euw.op.gg/summoner/userName=arakniro
# https://wol.gg/stats/euw/arakniro/
# https://steamcommunity.com/id/bullshit/games/?tab=all

"""
pseudo = input('Entrer le pseudo que vous rechercher :')
print("Joueur : " + pseudo)
soup = HttpRequest().get_url("https://euw.op.gg/summoner/userName=" + pseudo)
print(soup.find("div", class_="TierRank").text.strip())
soup = HttpRequest().get_url("https://wol.gg/stats/euw/" + pseudo + "/")
print(soup.find("div", id="time-hours").text.strip())
"""

soup = HttpRequest().get_url("https://steamcommunity.com/id/bullshit")
#print(soup.findAll())

def get_steam_site(username):
    """ Returns the URL of the steam community site given a username
    Parameters
    ----------
    username : str
        The user username
    """
    return ''.join(['https://steamcommunity.com/id/',username,'/games/?tab=all'])

def get_lol_site(username):
    """ Returns the URL of the lol site given a username

    Parameters
    ----------
    username : str
        The user username
    """
    return ''.join(['https://euw.op.gg/summoner/userName=',username])

def get_wol_site(country,username):
    """ Returns the URL of the wol site given a username

    Parameters
    ----------
    username : str
        The user username

    Returns
    ----------
    username : str
        The user username
    """
    return ''.join(['https://wol.gg/stats/',country,'/',username])

steam_soup = HttpRequest().get_url(get_steam_site('bullshit'))

page_content = steam_soup.find("div",attrs={"class": "responsive_page_content"})

main_content_soup = page_content.find("div",{'class':'maincontent'})

mainContents_soup = main_content_soup.find("div",{'id':'mainContents'})

games_list_soup = mainContents_soup.find('div',{'class':'games_list'})

games_list_container_soup = games_list_soup.find("div",{'id':'games_list_row_container'})

games_rows = games_list_container_soup.find("div",{'id':'games_list_rows'})

print(games_rows)