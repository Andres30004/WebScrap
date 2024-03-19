from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.service import Service as BaseService
import time
import pandas as pd

# Opciones de navegacion
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

# Ubicacion de chromedriver
driver_path = 'C:\\Users\\ANDRES\\Desktop\\chromedriver-win64\\chromedriver.exe'
service = ChromeService(executable_path=driver_path) if BaseService.start == ChromeService.start else BaseService(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Abre la pestaña de donde extraeremos información
driver.get('https://twitter.com/i/flow/login')

# Coloca los datos de usuario
user = "4ndr3s_3004"
input_user = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@name="text"]')))
input_user.send_keys(user)
input_user.send_keys(Keys.ENTER)

# Coloca la contraseña del usuario
campo_password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
campo_password.send_keys("Tati3004$")
campo_password.send_keys(Keys.ENTER)

# Abre la barra de búsqueda y busca a nuestro subjet
subjet = "Elon Musk"
search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")))
search_box.send_keys(subjet)
search_box.send_keys(Keys.ENTER)

people = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'People')]")))
people.click()

profile = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div[1]/a/div/div[1]/span/span[1]")))
profile.click()
time.sleep(5)

def scrape_tweets(driver, max_tweets=10):
    tweets = set()

    while len(tweets) < max_tweets:
        articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        
        for article in articles:
            tweet = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
            tweets.add(tweet)

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet']")))  # Esperar a que aparezcan más tweets

    return list(tweets)[:max_tweets]

# Uso de la función
scraped_tweets = scrape_tweets(driver)


print("numero de tweets",len(scraped_tweets))

# Crear un DataFrame
df = pd.DataFrame({'Tweets': scraped_tweets})

# Imprimir el DataFrame
print(df)

# Guardar el DataFrame como CSV
df.to_csv('tweets.csv', index=False)

# Cerrar el navegador al final
driver.quit()
