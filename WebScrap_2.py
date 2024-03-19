import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def login_twitter(driver, username, password):
    driver.get('https://twitter.com/i/flow/login')
    time.sleep(2)
    
    input_user = driver.find_element(By.XPATH, '//input[@name="text"]')
    input_user.send_keys(username)
    input_user.send_keys(Keys.ENTER)
    time.sleep(2)

    campo_password = driver.find_element(By.XPATH, '//input[@name="password"]')
    campo_password.send_keys(password)
    campo_password.send_keys(Keys.ENTER)
    time.sleep(2)

def search_and_scrape_tweets(driver, username, num_tweets=10):
    # Buscar el usuario
    search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
    search_box.send_keys(username)
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)

    people = driver.find_element(By.XPATH, "//span[contains(text(),'People')]")
    people.click()
    time.sleep(2)

    # Hacer clic en el perfil
    profile = driver.find_element(By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div[1]/a/div/div[1]/span/span[1]")
    profile.click()
    time.sleep(2)

    # Scraping de tweets
    df_tweets = scrape_tweets(driver, num_tweets)

    return df_tweets

def scrape_tweets(driver, num_tweets):
    Tweets = []
    
    def scroll_and_scrape():
        articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        for article in articles:
            tweet_text = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
            Tweets.append(tweet_text)
        
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(4)

    while len(set(Tweets)) < num_tweets:
        scroll_and_scrape()

    # Crear un DataFrame
    df = pd.DataFrame({'Tweets': Tweets[:num_tweets]})

    return df

# Uso del código
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

driver_path = 'C:\\Users\\ANDRES\\Desktop\\chromedriver-win64\\chromedriver.exe'
service = webdriver.ChromeService(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Iniciar sesión en Twitter
login_twitter(driver, "4ndr3s_3004", "Tati3004$")

# Obtener DataFrame de tweets para un usuario específico (por ejemplo, Elon Musk)

df_tweets_claud = search_and_scrape_tweets(driver, "claudiashein")
df_tweets_xoch = search_and_scrape_tweets(driver, "xochitlgalvez")
# Mostrar el DataFrame
print(df_tweets_claud)
print(df_tweets_xoch)


# Cerrar el navegador al finalizar
driver.quit()
