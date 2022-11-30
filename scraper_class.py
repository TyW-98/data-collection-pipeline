import requests 
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

hotel_dict = {"Hotel Name" : [], "Hotel Rating" : [], "Price/Night" : [], "Address": [], "Hotel URL": []}

driver = webdriver.Chrome()
driver.get("https://www.agoda.com/?cid=1844104")

time.sleep(10)

try:
    driver.find_elements(by= By.XPATH, value = '//button[@class = "ab-message-button"]')[1].click()
    time.sleep(2)
except:
    pass

destination = "Penang"
search_bar = driver.find_element(by = By.XPATH, value = '//*[@class = "SearchBoxTextEditor SearchBoxTextEditor--autocomplete"]')
search_bar.send_keys(destination)
driver.find_element(by = By.XPATH, value = '//button[@class = "Buttonstyled__ButtonStyled-sc-5gjk6l-0 hvHHEO Box-sc-kv6pi1-0 fDMIuA"]').click()
time.sleep(5)

hotel_list = [] 

all_hotel = driver.find_elements(by = By.XPATH, value = '//*[@class ="PropertyCard__Link"]')
for hotel in all_hotel:
    hotel_link = hotel.get_attribute("href")
    hotel_list.append(hotel_link)
    
for hotel in hotel_list:
    driver.get(hotel)
    hotel_page = requests.get(hotel)
    hotel_page = BeautifulSoup(hotel_page.content, "html.parser")
    print(hotel)
    hotel_name = driver.find_element(by = By.XPATH, value = '//*[@data-selenium = "hotel-header-name"]').text
    hotel_rating = driver.find_elements(by = By.XPATH, value = '//h3[@class = "Typographystyled__TypographyStyled-sc-j18mtu-0 hTkvyT kite-js-Typography "]')[0].text
    hotel_dict["Hotel Name"].append(hotel_name)
    hotel_dict["Hotel URL"].append(hotel)
    print(hotel_rating)
    print(hotel_name)
    time.sleep(5)
    
print(hotel_list)