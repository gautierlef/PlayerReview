#%%
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

#%%

def get_lol_site(username):
    return ''.join(['https://euw.op.gg/summoner/userName=',username])

#%%

wd_lol = webdriver.Chrome(executable_path="./chromedriver_win32/chromedriver.exe")
#%%
wd_lol.switch_to_window('/summoner/league/')

#%%
wd_lol.get(get_lol_site('arakniro'))

rank = wd_lol.find_element_by_class_name("LadderRank")


#%%
num_classement, tier_classement = rank.text.split(' ')[2:4]
#%%
num_classement = int(''.join([i for i in num_classement if i.isdigit()]))
#%%
tier_classement = float(''.join([i for i in tier_classement if i not in ['(','%']]))

#%%

classement_solo = wd_lol.find_element_by_class_name('TierRank')
classement_solo.text

#%%
classement_flex = wd_lol.find_element_by_class_name('sub-tier__rank-tier')
classement_flex.text

#%%

menu = wd_lol.find_element_by_class_name('Menu')
#%%
links = wd_lol.find_elements_by_css_selector('dd')
len(links)
#%%

side_content = wd_lol.find_element_by_class_name('SideContent')

#%%
win_ratio = wd_lol.find_element_by_class_name('WinRatioTitle')
#%%
nb_parties,nb_victoires,nb_defaites = win_ratio.text.split(' ').join([i for i in win_ratio.text if i.isdigit()])


#%%
''.join([i for i in win_ratio.text if i.isdigit()])