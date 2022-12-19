import requests 
import time
import datetime
import os
import json
import shutil
from calendar import monthrange
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

class hotel_finder:
    """Hotel information retriever for agoda.com
    
    This class retrieves information from agoda.com using selenium webdriver together with chromedriver to control the webbrowser. 
    
    Args:
        holiday_location (str): the location of the holiday destination 
        start_date (str): the start date of the holiday using the date format dd/mm/year
        number_of_nights (int): the number of nights planning to stay at the hotel
        number_of_hotels (int): how many hotel listings to scrape 
        
    """

    def __init__(self,holiday_location,start_date,number_of_nights,number_of_hotels):
        """
        see help(hotel_finder) for all th details
        """
        self.hotel_dict = {"Hotel ID": [],"Hotel Name" : [], "Hotel Rating" : [], "Price/Night" : [], "Address": [], "Hotel URL": [],"Hotel Pictures": [],"Time Scraped": []}
        self.holiday_location = holiday_location
        self.start_date = start_date
        self.number_of_nights = number_of_nights
        self.number_of_hotels = number_of_hotels
        self.hotel_list = []
        self.hotel_id_list = []
        self.working_directory = os.path.dirname(os.path.realpath(__file__)).replace('\\',"/")
        
        self.load_main_page()
        self.hotel_location_search()
        self.page_scroller()
        self.hotel_listing()
        self.hotel_details()
    
    def load_main_page(self):
        """loads the main page of agoda.com

        This function uses selenium webdriver to load the home page of agoda.com.
        After loading agoda's home page it will then try to close the pop up ad
        which always shows up everytime when visiting the page. It will also store
        the default selected currency. 
        """
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options = chrome_options)
        self.driver.get("https://www.agoda.com/") 
        time.sleep(7)
        
        try:
            self.driver.find_elements(by= By.XPATH, value = '//button[@class = "ab-message-button"]')[1].click()   
            time.sleep(2)
        except:
            pass
        
        self.currency = self.driver.find_element(by = By.XPATH, value = '//p[@class = "Typographystyled__TypographyStyled-sc-j18mtu-0 gSVfcd kite-js-Typography CurrencyContainer__SelectedCurrency__Symbol"]').text
        
    def hotel_location_search(self):
        """Search holiday destination
        
        This function enters the user's holiday destination into the search bar and
        filters the listings to show hotels and resorts only.
        """
        time.sleep(5)    
        
        search_bar = self.driver.find_element(by = By.XPATH, value = '//*[@class = "SearchBoxTextEditor SearchBoxTextEditor--autocomplete"]')
        search_bar.send_keys(self.holiday_location)
        
        time.sleep(2.5)
        search_bar.send_keys(Keys.ENTER)
        
        self.select_holiday_date()
        time.sleep(2.5)
        
        search_bar.send_keys(Keys.ESCAPE)
        time.sleep(2.5)
        
        self.driver.find_element(by = By.XPATH, value = '//button[@class = "Buttonstyled__ButtonStyled-sc-5gjk6l-0 hKHQVh Box-sc-kv6pi1-0 fDMIuA"]').click()        
        time.sleep(5)
        
        self.driver.find_element(by = By.XPATH, value = '//*[@class = "filter-btn more-less-btn"]').click()
        time.sleep(2.5)
        
        hotel_tick_box = self.driver.find_element(by = By.XPATH, value = '//*[@class="filter-item-info AccomdType-34 "]')
        hotel_tick_box.find_element(by = By.CLASS_NAME, value = "checkbox-icon").click()
        time.sleep(3)
        resort_tick_box = self.driver.find_element(by = By.XPATH, value = '//*[@class = "filter-item-info AccomdType-37 "]')
        resort_tick_box.find_element(by = By.CLASS_NAME, value = "checkbox-icon").click()
        time.sleep(5)
        
    def set_holiday_dates(self):
        selected_start_date, selected_month, selected_year = (n for n in self.start_date.split("/"))
        number_of_days_in_start_date_month = monthrange(int(selected_year),int(selected_month))[1]
        end_day = int(selected_start_date) + self.number_of_nights
        
        if number_of_days_in_start_date_month - end_day < 0:
            end_day -= number_of_days_in_start_date_month
            selected_month = int(selected_month) + 1
            if selected_month == 13:
                selected_month = 1
                selected_year = int(selected_year) + 1
   
        end_date = f"{end_day}/{selected_month}/{selected_year}"
       
        holiday_dates = {"start of holiday": self.start_date,"end of holiday": end_date}
        
        return holiday_dates
            
    def set_date(self,date):      
        holiday_start_day, holiday_month, holiday_year = date.split("/")
        
        month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8 , "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        week_dict = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
        
        holiday_month_str = list(month_dict.keys())[list(month_dict.values()).index(int(holiday_month))]
        
        time.sleep(2.5)
        all_months = self.driver.find_elements(by = By.XPATH, value = '//*[@class = "DayPicker-Caption DayPicker-Caption-Wide"]')            
        currently_display_year = [year.text.split(" ")[1] for year in all_months]
        currently_display_months = [month.text.split(" ")[0][:3] for month in all_months]
        
        print(currently_display_months ,currently_display_year)
        
        while holiday_month_str not in currently_display_months:
            
            self.driver.find_element(by = By.XPATH, value = '//*[@class = "DayPicker-NavButton DayPicker-NavButton--next  ficon ficon-18 ficon-edge-arrow-right"]').click()
            time.sleep(2.5)
            
            currently_display_months = []
            currently_display_year = []
            
            all_months = self.driver.find_elements(by = By.XPATH, value = '//*[@class = "DayPicker-Caption DayPicker-Caption-Wide"]')
            currently_display_year = [year.text.split(" ")[1] for year in all_months]
            currently_display_months = [month.text.split(" ")[0][:3] for month in all_months]
            
        number_of_days_in_holiday_month = monthrange(int(holiday_year),int(holiday_month))[1]
        number_of_days_in_display_month_1 = monthrange(int(currently_display_year[0]),list(month_dict.values())[list(month_dict.keys()).index(currently_display_months[0])])[1]
        number_of_days_in_display_month_2 = monthrange(int(currently_display_year[1]),list(month_dict.values())[list(month_dict.keys()).index(currently_display_months[1])])[1]
        all_days_element = self.driver.find_elements(by = By.XPATH, value = '//*[@class = "PriceSurgePicker-Day__label PriceSurgePicker-Day__label--wide"]')   
        
        month_position = currently_display_months.index(holiday_month_str)
        
        if month_position == 0:
            all_days_element = all_days_element[:number_of_days_in_holiday_month-1]
        else:
            all_days_element = all_days_element[number_of_days_in_display_month_1-1:]
             
        for days in all_days_element:
            
            if days.text == holiday_start_day:
                
                days_parent = days.find_element(by = By.XPATH, value = '..')  
                days_parent = days_parent.find_element(by = By.XPATH, value = '..')
                days_parent = days_parent.find_element(by = By.XPATH, value = '..')
                days_parent.click()
                time.sleep(2.5)
                break
                
    def select_holiday_date(self):
        
        holiday_dates = self.set_holiday_dates()
        
        for key_dates in list(holiday_dates.keys()):
            self.set_date(holiday_dates[key_dates])
            time.sleep(5)
        
            
    def page_scroller(self):
        """Scroll hotel listing page

        As the hotel listing page is dynamically loaded in, an infinite scroll
        function is implemented in order to load all the hotel listings in the
        listing page. The scroll function stores the page height in the variable
        named page_height and new_height and this two variables will keep updated
        as the page is being scrolled. The function will terminate when both the
        variables is equals to each other. 
        """
        
        page_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight/2);")
            
            time.sleep(6)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == page_height:
                
                self.driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
                
                break
            
            page_height = new_height
            
    def hotel_listing(self):
        """Obtain all hotel listings

        This functions collects the details page and unique ID of all the hotels listed in the listing page and append it it to a list.
        """

        all_hotel = self.driver.find_elements(by = By.XPATH, value = '//*[@class ="PropertyCard__Link"]')
        all_hotel_id = self.driver.find_elements(by = By.XPATH, value = '//*[@data-selenium = "hotel-item"]')
        
        for hotel, hotel_id in zip(all_hotel, all_hotel_id):
            hotel_link = hotel.get_attribute("href")
            self.hotel_list.append(hotel_link)
            self.hotel_id_list.append(hotel_id.get_attribute("data-hotelid"))
            
    def file_path(self,hotel_name,hotel_id):
        """Hotel folder directory 

        This function gets the hotel folder directiory using the hotel's name and its unique id.

        Args:
            hotel_name (str): the name of the hotel
            hotel_id (int): the unique ID number associated with the hotel 

        Returns:
            str: the full working path 
        """
        
        folder_name = f"{hotel_name} (hotel ID - {hotel_id})"
        full_path = f"{self.working_directory}/raw data/{self.holiday_location}/{folder_name}"
        
        return full_path
            
    def hotel_details(self):
        
        hotel_dict_keys = list(self.hotel_dict.keys())
        
        if self.number_of_hotels != 99:
            self.hotel_list = self.hotel_list[:self.number_of_hotels]
        
        for hotel_number , hotel in enumerate(self.hotel_list):
            individual_hotel_dict = dict.fromkeys(hotel_dict_keys, 0)
            self.driver.get(hotel)
            hotel_page = requests.get(hotel)
            time.sleep(6) 
            
            current_time = self.get_current_time()
            self.hotel_dict["Time Scraped"].append(current_time)
            individual_hotel_dict["Time Scraped"] = current_time
            
            hotel_id = int(self.hotel_id_list[hotel_number])      
            hotel_name = self.driver.find_element(by = By.XPATH, value = '//*[@data-selenium = "hotel-header-name"]').text
            hotel_rating = float(self.driver.find_elements(by = By.XPATH, value = '//h3[@class = "Typographystyled__TypographyStyled-sc-j18mtu-0 hTkvyT kite-js-Typography "]')[0].text)
            hotel_address = self.driver.find_element(by = By.XPATH, value = '//*[@data-selenium = "hotel-address-map"]').text
            check_hotel_room_avaliability = self.driver.find_elements(by = By.XPATH, value = '//*[@class = "Spanstyled__SpanStyled-sc-16tp9kb-0 gwICfd kite-js-Span pd-price PriceDisplay PriceDisplay--noPointer PriceDisplay pd-color"]')
            
            if check_hotel_room_avaliability == []:
                hotel_price_per_night = "No rooms avaliable"
            else:
                hotel_price_per_night = float(check_hotel_room_avaliability[0].find_element(by = By.XPATH, value = '//strong[@data-ppapi = "room-price"]').text)
        
            hotel_url = self.driver.current_url
            details_list = [hotel_id, hotel_name, hotel_rating, hotel_price_per_night, hotel_address, hotel_url]
            
            for detail, dict_key in zip(details_list, hotel_dict_keys[:7]):
                self.hotel_dict[dict_key].append(detail)
                individual_hotel_dict[dict_key] = detail
            
            self.full_path = self.file_path(hotel_name,hotel_id)
            
            picture_url_list = self.get_picture()
            
            individual_hotel_dict["Hotel Pictures"] = picture_url_list
            
            self.save_data(individual_hotel_dict)
            
            print(self.hotel_dict)
    
            time.sleep(5)  
            
            
    def get_current_time(self):
        """Get current time

        Get the current time and date in ISO format but with microseconds replaced to 0.

        Returns:
            str: the current time and date in ISO format
            
        """
        current_time = datetime.datetime.now().replace(microsecond=0).isoformat()
        
        return current_time
                 
        
    def get_picture(self):
        """Get all hotel picture's source

        This function gets the source of all the hotel images posted on the hotel's
        details' page.

        Returns:
            list: returns a list of all the hotel's images source.
        """
        
        time.sleep(5)
        
        hotel_picture_url_list = []
        
        see_all_pictures_button = self.driver.find_element(by = By.XPATH, value = '//*[@data-element-name = "hotel-mosaic-see-all-photos"]')
        see_all_pictures_button.find_element(by = By.TAG_NAME, value = "button").click()
                                                           
        time.sleep(7)
        
        hotel_thumbnails = self.driver.find_elements(by = By.XPATH, value = '//*[@data-element-name = "hotel-gallery-thumbnail"]')
        
        for picture_number, picture in enumerate(hotel_thumbnails):
            picture_url = picture.find_element(by = By.TAG_NAME, value = "img")    
            picture_url = picture_url.get_attribute("src")
            self.download_picture(picture_url,picture_number)
            hotel_picture_url_list.append(picture_url)   
            
        self.hotel_dict["Hotel Pictures"].append(hotel_picture_url_list)
        
        return hotel_picture_url_list
          
    def download_picture(self, picture_url, image_number):
        """download all hotel images

        Download all the hotel images posted on their repesctive details page and
        store it in their individual folders. The images will be renamed to the the following format: "<current date>_<current time>_<image number>.png"

        Args:
            picture_url (str): the source of the image
            image_number (int): the current image index
        """
        
        image_folder_dir = f"{self.full_path}/images"
        if image_number == 0 and os.path.exists(image_folder_dir):
            shutil.rmtree(image_folder_dir)
            os.makedirs(image_folder_dir) 
        elif image_number == 0 and not os.path.exists(image_folder_dir):
            os.makedirs(image_folder_dir)
            
        image_data = requests.get(picture_url).content
        current_time = self.get_current_time()
        current_date = current_time.split("T")[0]
        current_time = current_time.split("T")[1]
        hr, minute, seconds = current_time.split(":")
        current_time = f"{hr}hr{minute}min{seconds}sec"
        
        image_dir = r"{}/{}_{}_{}".format(image_folder_dir, current_date, current_time, image_number)
        
        with open(image_dir + ".png","wb") as img:
            img.write(image_data)

    def save_data(self,current_hotel_dict):
        """save hotel data

        Save the individual hotel data to json file.

        Args:
            current_hotel_dict (dict): contains all the current hotel information.
        """

        if not os.path.exists(self.full_path):
            os.makedirs(self.full_path)
        
        with open(f"{self.full_path}/data.json", "w") as json_file:
            json.dump(current_hotel_dict,json_file)

    def __str__(self):
        return f"Hotel finder for {self.holiday_location}"
    
if __name__ == "__main__":
    destination = "Penang"
    number_of_hotels = 5
    start_date = "31/12/2022"
    number_of_nights = 15
    
    all_hotels = hotel_finder(destination,start_date,number_of_nights,number_of_hotels)
    
    print(all_hotels)
    
