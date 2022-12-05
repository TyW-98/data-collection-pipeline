import requests 
import time
import datetime
from calendar import monthrange
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

class hotel_finder:

    def __init__(self,holiday_location,start_date,number_of_nights,pages):
        self.hotel_dict = {"Hotel ID": [],"Hotel Name" : [], "Hotel Rating" : [], "Price/Night" : [], "Address": [], "Hotel URL": [],"Hotel Pictures": [],"Time Scraped": []}
        self.holiday_location = holiday_location
        self.start_date = start_date
        self.number_of_nights = number_of_nights
        self.pages = pages + 1
        self.hotel_list = []
        self.hotel_id_list = []
        
        self.load_main_page()
        self.hotel_location_search()
        self.page_scroller()
        self.hotel_listing()
        self.hotel_details()
    
    def load_main_page(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(options = chrome_options)
        self.driver.get("https://www.agoda.com/") 
        time.sleep(10)
        
        try:
            self.driver.find_elements(by= By.XPATH, value = '//button[@class = "ab-message-button"]')[1].click()   
            time.sleep(2)
        except:
            pass
        
    def hotel_location_search(self):
            
        search_bar = self.driver.find_element(by = By.XPATH, value = '//*[@class = "SearchBoxTextEditor SearchBoxTextEditor--autocomplete"]')
        search_bar.send_keys(self.holiday_location)
        
        #time.sleep(2.5)
        #search_bar.send_keys(Keys.ENTER)
        #self.set_date()
        
        self.driver.find_element(by = By.XPATH, value = '//button[@class = "Buttonstyled__ButtonStyled-sc-5gjk6l-0 hvHHEO Box-sc-kv6pi1-0 fDMIuA"]').click()        
        time.sleep(10)
        
        self.driver.find_element(by = By.XPATH, value = '//*[@class = "filter-btn more-less-btn"]').click()
        time.sleep(2.5)
        
        hotel_tick_box = self.driver.find_element(by = By.XPATH, value = '//*[@class="filter-item-info AccomdType-34 "]')
        hotel_tick_box.find_element(by = By.CLASS_NAME, value = "checkbox-icon").click()
        time.sleep(3)
        resort_tick_box = self.driver.find_element(by = By.XPATH, value = '//*[@class = "filter-item-info AccomdType-37 "]')
        resort_tick_box.find_element(by = By.CLASS_NAME, value = "checkbox-icon").click()
        time.sleep(10)
        
    def set_date(self) :
        
        #self.driver.find_element(by = By.XPATH, value = '//*[@class = "IconBox IconBox--checkIn"]').click()
        time.sleep(5)
        
        all_months = self.driver.find_elements(by = By.XPATH, value = '//*[@class ="DayPicker-Caption DayPicker-Caption-Wide"]')
        
        month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8 , "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        week_dict = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
        
        selected_start_date, selected_month, selected_year = (n for n in self.start_date.split("/"))
        selected_end_date = int(selected_start_date) + number_of_nights
        weekday = datetime.date(year = int(selected_year), month = int(selected_month), day = int(selected_start_date)).weekday()
        selected_month = list(month_dict.keys())[list(month_dict.values()).index(int(selected_month))]
        weekday = list(week_dict.keys())[list(week_dict.values()).index(weekday)]
        
        for months in all_months:
            current_month = months.text
            total_number_of_days = monthrange(int(selected_year),month_dict[current_month[:3]])
            #date_label = f"{weekday} {selected_month} {selected_start_date} {selected_year}"               
            if selected_month == current_month[:3] and int(selected_year) == int(current_month[-4:]):
                days_element = self.driver.find_elements(by = By.XPATH, value = '//*[@class = "PriceSurgePicker-Day__label PriceSurgePicker-Day__label--wide"]')
                for days in days_element[:total_number_of_days[1]-1]:
                    print(days.text)
                    if days.text == selected_start_date or days.text == selected_end_date:
                        days_parent = days.find_element(by = By.XPATH, value = '..')  
                        days_parent = days_parent.find_element(by = By.XPATH, value = '..')
                        days_parent = days_parent.find_element(by = By.XPATH, value = '..')
                        days_parent.click()
                        time.sleep(15)   
                        continue
                    else:
                        pass
            else:
                pass
            
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
        all_hotel_id = self.driver.find_elements(by = By.XPATH, value = '//*[@data-selenium = "hotel-item"]')
        
        for hotel, hotel_id in zip(all_hotel, all_hotel_id):
            hotel_link = hotel.get_attribute("href")
            self.hotel_list.append(hotel_link)
            self.hotel_id_list.append(hotel_id.get_attribute("data-hotelid"))
            
            
    def hotel_details(self):
        
         for n , hotel in enumerate(self.hotel_list):
            self.driver.get(hotel)
            hotel_page = requests.get(hotel)
            time.sleep(10)
            hotel_page = BeautifulSoup(hotel_page.content, "html.parser")    
            
            self.get_current_time()
                    
            hotel_name = self.driver.find_element(by = By.XPATH, value = '//*[@data-selenium = "hotel-header-name"]').text
            hotel_rating = self.driver.find_elements(by = By.XPATH, value = '//h3[@class = "Typographystyled__TypographyStyled-sc-j18mtu-0 hTkvyT kite-js-Typography "]')[0].text
            hotel_address = self.driver.find_element(by = By.XPATH, value = '//*[@data-selenium = "hotel-address-map"]').text
            price_per_night = self.driver.find_element(by =By.XPATH, value = '//strong[@data-ppapi = "room-price"]').text
            self.hotel_dict["Hotel ID"].append(self.hotel_id_list[n])
            self.hotel_dict["Hotel Name"].append(hotel_name)
            self.hotel_dict["Hotel URL"].append(hotel)
            self.hotel_dict["Hotel Rating"].append(hotel_rating)
            self.hotel_dict["Address"].append(hotel_address)
            self.hotel_dict["Price/Night"].append(price_per_night)
        
            self.get_picture()
            
            print(price_per_night)
            print(self.hotel_dict)
    
            time.sleep(5)  
            
    def get_current_time(self):
        
        current_time = datetime.datetime.now().replace(microsecond=0).isoformat()
        self.hotel_dict["Time Scraped"].append(current_time)
                 
            
    def get_picture(self):
        
        time.sleep(10)
        
        hotel_picture_url_list = []
        
        see_all_pictures_button = self.driver.find_element(by = By.XPATH, value = '//*[@data-element-name = "hotel-mosaic-see-all-photos"]')
        see_all_pictures_button.find_element(by = By.TAG_NAME, value = "button").click()
                                                           
        time.sleep(15)
        
        hotel_thumbnails = self.driver.find_elements(by = By.XPATH, value = '//*[@data-element-name = "hotel-gallery-thumbnail"]')
        
        for picture in hotel_thumbnails:
            picture_url = picture.find_element(by = By.TAG_NAME, value = "img")    
            picture_url = picture_url.get_attribute("src")
            hotel_picture_url_list.append(picture_url)   
            
        self.hotel_dict["Hotel Pictures"].append(hotel_picture_url_list)
    
    def __str__(self):
        return f"Hotel finder for {self.holiday_location}"
    
if __name__ == "__main__":
    destination = "Penang"
    number_of_pages = 3
    start_date = "20/12/2022"
    number_of_nights = 4
    
    penang_hotel = hotel_finder(destination,start_date, number_of_nights ,number_of_pages)
    
    print(penang_hotel)
    

