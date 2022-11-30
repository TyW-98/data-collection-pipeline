import requests 
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

class hotel_finder:

    hotel_dict = {"Hotel Name" : [], "Hotel Rating" : [], "Price/Night" : [], "Address": [], "Hotel URL": []}

    def __init__(self,holiday_location,pages):
        self.holiday_location = holiday_location
        self.pages = pages + 1
        
    def scraper(self):
        driver = webdriver.Chrome()
        driver.get("https://www.agoda.com/?cid=1844104")
        time.sleep(10)
        
        try:
            driver.find_elements(by= By.XPATH, value = '//button[@class = "ab-message-button"]')[1].click()
            time.sleep(2)
        except:
            pass        
        
        search_bar = driver.find_element(by = By.XPATH, value = '//*[@class = "SearchBoxTextEditor SearchBoxTextEditor--autocomplete"]')
        search_bar.send_keys(self.holiday_location)
        driver.find_element(by = By.XPATH, value = '//button[@class = "Buttonstyled__ButtonStyled-sc-5gjk6l-0 hvHHEO Box-sc-kv6pi1-0 fDMIuA"]').click()
        time.sleep(10)
        
        for n in range(self.pages):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(30)
        
        
        hotel_list = [] 

        all_hotel = driver.find_elements(by = By.XPATH, value = '//*[@class ="PropertyCard__Link"]')
        for hotel in all_hotel:
            hotel_link = hotel.get_attribute("href")
            hotel_list.append(hotel_link)
            
        for hotel in hotel_list:
            driver.get(hotel)
            hotel_page = requests.get(hotel)
            hotel_page = BeautifulSoup(hotel_page.content, "html.parser")
            hotel_name = driver.find_element(by = By.XPATH, value = '//*[@data-selenium = "hotel-header-name"]').text
            hotel_rating = driver.find_elements(by = By.XPATH, value = '//h3[@class = "Typographystyled__TypographyStyled-sc-j18mtu-0 hTkvyT kite-js-Typography "]')[0].text
            hotel_address = driver.find_element(by = By.XPATH, value = '//*[@data-selenium = "hotel-address-map"]').text
            ppn = driver.find_element(by =By.XPATH, value = '//strong[@data-ppapi = "room-price"]').text
            self.hotel_dict["Hotel Name"].append(hotel_name)
            self.hotel_dict["Hotel URL"].append(hotel)
            self.hotel_dict["Hotel Rating"].append(hotel_rating)
            self.hotel_dict["Address"].append(hotel_address)
            self.hotel_dict["Price/Night"].append(ppn)
            print(ppn)
            time.sleep(5)       
            
        return self.hotel_dict
    
    def __str__(self):
        return f"Hotel finder for {self.holiday_location}"

destination = "Penang"
number_of_pages = 3

Penang_hotel = hotel_finder(destination,number_of_pages).scraper()

print(Penang_hotel)
