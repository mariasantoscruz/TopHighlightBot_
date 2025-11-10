#pip3 install -U selenium
#pip3 install webdriver-manager
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://tacobell.es/")
time.sleep(3)
element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/ngb-modal-window/div/div/div/div/div[2]/button[1]"))
    )
## Another way to find the element
#element = driver.find_element(By.XPATH,"/html/body/div[5]/div[3]/div/div/div[2]/div/div/button[2]")
element.click()

element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-full/div/div[2]/div[1]/app-main-menu/nav/ul/li[5]/a"))
    )

element.click()

## Other usefull commands:
#element.send_keys("hello")
#element.get_attribute("")
input()

element.send_keys("hola")
