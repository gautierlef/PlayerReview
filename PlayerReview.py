import requests
import re
from bs4 import BeautifulSoup


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


# https://euw.op.gg/summoner/userName=arakniro
# https://wol.gg/stats/euw/arakniro/
# https://steamcommunity.com/id/bullshit/games/?tab=all

"""print('Entrer le pseudo que vous rechercher :')
pseudo = input()
print("Joueur : " + pseudo)
soup = HttpRequest().get_url("https://euw.op.gg/summoner/userName=" + pseudo)
print(soup.find("div", class_="TierRank").text.strip())
soup = HttpRequest().get_url("https://wol.gg/stats/euw/" + pseudo + "/")
print(soup.find("div", id="time-hours").text.strip())"""
soup = HttpRequest().get_url("https://steamcommunity.com/id/bullshit")
print(soup.findAll())
