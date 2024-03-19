import requests #hacer peticion a la pagina
#from bs4 import BeautifulSoup as bs #permite extraer el html
import random 
import time #para hacer pausas
import pandas as pd
from selenium import webdriver #permite ser web scraping
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc #permite que las paginas no detecten que es un ordenador
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import pyodbc
from sqlalchemy import create_engine
import urllib
browser = webdriver.Chrome()

url= "https://twitter.com/i/flow/login"

browser.get(url)

time.sleep(10)

#browser.implicitly_wait(10)

user = "4ndr3s_3004"
password= "Tati3004"
username= ""
input_user=browser.find_element(By.XPATH,'//input[@name="text"]')
input_user.send_keys(user)
input_user.send_keys(Keys.ENTER)
time.sleep(5)
input_username=browser.find_element(By.XPATH, '//input[@name="text" and @data-testid="ocfEnterTextTextInput"]')
input_username.send_keys(username)
input_username.send_keys(Keys.ENTER)
time.sleep(5)
campo_password= browser.find_element(By.XPATH, '//input[@name="password"]')
campo_password.send_keys(password)
campo_password.send_keys(Keys.ENTER)
time.sleep(5)



def extract_single_tweet():
    # Lista para almacenar el tweet
    global browser
    Tweets = []
   
    
        # Encontrar el elemento del tweet
    tweet_element = browser.find_element(By.XPATH, "//div[@data-testid='tweetText']")

        # Hacer scroll hasta el elemento del tweet
    browser.execute_script("arguments[0].scrollIntoView();", tweet_element)

        # Esperar a que ocurran cambios en la página después del clic
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='tweetText']")))

    time.sleep(2)

    #post = browser.find_element(By.XPATH,
    post = browser.find_element(By.XPATH,"//article[@data-testid='tweet']")
    post.click()
    time.sleep(5)
        # Extraer el texto del tweet
    tweet_text = tweet_element.text
    Tweets.append(tweet_text)
    return Tweets
    
def extract_comments(browser, max_comments=30):
    Comments = []

    while True:
        articles = browser.find_elements(By.XPATH, "//article[@data-testid='tweet']")

        
        for article in articles:
            # Extraer comentarios de cada tweet
            comments_elements = article.find_elements(By.XPATH, ".//div[@data-testid='tweetText']")
            for comment_element in comments_elements:
                comment_text = comment_element.text
                Comments.append(comment_text)

        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        # Esperar a que cargue la página después de desplazar
        time.sleep(4)

        articles = browser.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        if len(Comments) >= max_comments:
            break

    return Comments

 

# Perfil 1: Claudia Sheinbaum
subject1 = "Claudia Sheinbaum"
search_box = browser.find_element(By.XPATH, '//input[@data-testid="SearchBox_Search_Input"]')
search_box.send_keys(subject1)
search_box.send_keys(Keys.ENTER)
time.sleep(4)

people = browser.find_element(By.XPATH, "//span[contains(text(),'Personas')]")
people.click()
time.sleep(3)

profile = browser.find_element(By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]")
profile.click()
time.sleep(5)

tweets_profile1 = extract_single_tweet()
tweets_profile1 = extract_comments(browser)

# Volver a la página de inicio
browser.get("https://twitter.com/home")

time.sleep(5)

# Perfil 2: Otro perfil
subject2 = "Xochitl Galvez"
search_box = browser.find_element(By.XPATH, '//input[@data-testid="SearchBox_Search_Input"]')
search_box.send_keys(subject2)
search_box.send_keys(Keys.ENTER)
time.sleep(4)

people = browser.find_element(By.XPATH, "//span[contains(text(),'Personas')]")
people.click()
time.sleep(3)

profile = browser.find_element(By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span")
profile.click()
time.sleep(5)

tweets_profile2 = extract_single_tweet()
tweets_profile2 = extract_comments(browser)