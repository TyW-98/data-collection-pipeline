import requests 
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

class hotel_finder:

    def __init__(self,holiday_location,pages):
        self.hotel_dict = {"Hotel Name" : [], "Hotel Rating" : [], "Price/Night" : [], "Address": [], "Hotel URL": []}
        self.holiday_location = holiday_location
        self.pages = pages + 1
        self.hotel_list = []
        
        self.load_main_page()
        self.hotel_location_search()
        self.page_scroller()
        self.hotel_listing()
        self.hotel_details()
    
    def load_main_page(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.agoda.com/?cid=1844104") 
        time.sleep(10)
        
        try:
            self.driver.find_elements(by= By.XPATH, value = '//button[@class = "ab-message-button"]')[1].click()   
            time.sleep(2)
        except:
            pass
        
    def hotel_location_search(self):
            
        search_bar = self.driver.find_element(by = By.XPATH, value = '//*[@class = "SearchBoxTextEditor SearchBoxTextEditor--autocomplete"]')
        search_bar.send_keys(self.holiday_location)
        self.driver.find_element(by = By.XPATH, value = '//button[@class = "Buttonstyled__ButtonStyled-sc-5gjk6l-0 hvHHEO Box-sc-kv6pi1-0 fDMIuA"]').click()        
        time.sleep(10)
        
        hotel_tick_box = self.driver.find_element(by = By.XPATH, value = '//*[@class="filter-item-info AccomdType-34 "]')
        hotel_tick_box.find_element(by = By.CLASS_NAME, value = "checkbox-icon").click()
        time.sleep(10)
        resort_tick_box = self.driver.find_element(by = By.XPATH, value = '//*[@class = "filter-item-info AccomdType-37 "]')
        resort_tick_box.find_element(by = By.CLASS_NAME, value = "checkbox-icon").click()
            
    def page_scroller(self):
        
        page_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            time.sleep(6)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == page_height:
                
                self.driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
                
                break
            
            page_height = new_height
            
    def hotel_listing(self):

        all_hotel = self.driver.find_elements(by = By.XPATH, value = '//*[@class ="PropertyCard__Link"]')
        
        for hotel in all_hotel:
            hotel_link = hotel.get_attribute("href")
            self.hotel_list.append(hotel_link)
            
            
    def hotel_details(self):
        
         for hotel in self.hotel_list:
            self.driver.get(hotel)
            hotel_page = requests.get(hotel)
            hotel_page = BeautifulSoup(hotel_page.content, "html.parser")
            hotel_name = self.driver.find_element(by = By.XPATH, value = '//*[@data-selenium = "hotel-header-name"]').text
            hotel_rating = self.driver.find_elements(by = By.XPATH, value = '//h3[@class = "Typographystyled__TypographyStyled-sc-j18mtu-0 hTkvyT kite-js-Typography "]')[0].text
            hotel_address = self.driver.find_element(by = By.XPATH, value = '//*[@data-selenium = "hotel-address-map"]').text
            price_per_night = self.driver.find_element(by =By.XPATH, value = '//strong[@data-ppapi = "room-price"]').text
            self.hotel_dict["Hotel Name"].append(hotel_name)
            self.hotel_dict["Hotel URL"].append(hotel)
            self.hotel_dict["Hotel Rating"].append(hotel_rating)
            self.hotel_dict["Address"].append(hotel_address)
            self.hotel_dict["Price/Night"].append(price_per_night)
            print(price_per_night)
            time.sleep(5)           
    
    def __str__(self):
        return f"Hotel finder for {self.holiday_location}"
    
if __name__ == "__main__":
    destination = "Penang"
    number_of_pages = 3
    
    penang_hotel = hotel_finder(destination, number_of_pages)
    
    print(penang_hotel)
    

