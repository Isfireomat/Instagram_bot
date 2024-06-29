from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import random
from selenium.webdriver.common.by import By
import instaloader



def get_all_follovers(login,password,user_name):
    loader = instaloader.Instaloader()
    loader.login(login, password)
    profile = instaloader.Profile.from_username(loader.context, user_name)
    print("1")
    followers_with_stories = []
    try:
        for follower in profile.get_followers():
            print(follower.username)
            try:
                if follower.has_viewable_story:
                    followers_with_stories.append(follower.username)
            except Exception as E :print(E)
    except Exception as E :print(E)
    return followers_with_stories

def view_all_stories(driver,followers):
            

login= 'dfdfgfgf666'
password= ''

user_name='_artandcraft_17'

followers=get_all_follovers(login,password,user_name)
# followers=['_rajput__0976', 'sigma_amar_nath_09', 'eklaakh_786', 'skynoor_tour_and_travels', 'nigamkumar9706', 'masudi_atwabi', '__zainab15.__']\
# followers=['sadimshahzad']
if len(followers):
    service = webdriver.ChromeService(executable_path = "chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    authorize(driver,login,password)
    # test(driver)
    stories,all_stories=view_all_stories(driver,followers)
    print(f"Всего просмотрено людей с историями: {stories}\nВсего историй: {all_stories}")
# time.sleep(100)
# stories_count = get_stories_count(driver)
# print(stories_count)
# stories_count,all_stories_count=watch_stories(driver)
# print(f"Историй от разных людей: {stories_count}\nВсего историй: {all_stories_count}")