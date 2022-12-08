# Data Collection Pipeline

This project builds a scraper to collect data from [Agoda's website](https://www.agoda.com) an online travel agency's website which allows travellers to look for hotels, flights and activities at a specific holiday destination. By using `Selenium` package, this project will look for hotels and resorts at the user's specified destination which are listed on Agoda. 

```go
pip install selenium
```

## __Milestone 1__ 
* Setup of GitHub repository to store project files

## __Milestone 2__ 
* Select which website to collect data from, in this case [Agoda](https://www.agoda.com) was chosen.

## __Milestone 3__ 
* Create a scraper class which will contain all the methods that will be used to scrape data from the chosen website. 
* Create a method named `load_main_page` which will load the home page of the website and close the ad pop-ups which shows up at the home page everytime after several seconds. 
* The same method also records down the currency which is currently being displayed.

```go
def load_main_page(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(options = chrome_options)
        self.driver.get("https://www.agoda.com/") 
        time.sleep(7)
        
        try:
            self.driver.find_elements(by= By.XPATH, value = '//button[@class = "ab-message-button"]')[1].click()   
            time.sleep(2)
        except:
            pass
        
        self.currency = self.driver.find_element(by = By.XPATH, value = '//p[@class = "Typographystyled__TypographyStyled-sc-j18mtu-0 gSVfcd kite-js-Typography CurrencyContainer__SelectedCurrency__Symbol"]').text
```

* Create a method named `hotel_location_search` to enter the holiday location into the search bar and click the search button once the holiday location has been entered. 
* This method also filters out all the listing to hotels and resorts only by toggling the their repective checkboxes. 

```go
 def hotel_location_search(self):
            
        search_bar = self.driver.find_element(by = By.XPATH, value = '//*[@class = "SearchBoxTextEditor SearchBoxTextEditor--autocomplete"]')
        search_bar.send_keys(self.holiday_location)
        
        time.sleep(2.5)
        
        self.driver.find_element(by = By.XPATH, value = '//button[@class = "Buttonstyled__ButtonStyled-sc-5gjk6l-0 hvHHEO Box-sc-kv6pi1-0 fDMIuA"]').click()        
        time.sleep(5)
        
        # min_price_box = self.driver.find_element(by = By.XPATH, value = '//*[@id = "price_box_0"]')
        # min_price_box.send_keys("10")
        # time.sleep(2)
        
        self.driver.find_element(by = By.XPATH, value = '//*[@class = "filter-btn more-less-btn"]').click()
        time.sleep(2.5)
        
        hotel_tick_box = self.driver.find_element(by = By.XPATH, value = '//*[@class="filter-item-info AccomdType-34 "]')
        hotel_tick_box.find_element(by = By.CLASS_NAME, value = "checkbox-icon").click()
        time.sleep(3)
        resort_tick_box = self.driver.find_element(by = By.XPATH, value = '//*[@class = "filter-item-info AccomdType-37 "]')
        resort_tick_box.find_element(by = By.CLASS_NAME, value = "checkbox-icon").click()
        time.sleep(5)
```

* Since the hotel listing in the listing page is dynamically loaded in as the page is being scrolled, a method named `page_scroller` is used to scroll through the page in order to load all the hotel listings. 
* This method uses `page_height` and `new_height` to store the old and new height of the page. Only when `new_height` and `page_height` is the same as each other, the `page_scroller` will stop scrolling as this means the scroller has reached the bottom of the page and all the hotel listings for that page has been loaded in. 

```go 
 def page_scroller(self):
        
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
```
* The method named `hotel_listing` collects all the url associated with the hotels listed in the listing page. 

```go
def hotel_listing(self):

        all_hotel = self.driver.find_elements(by = By.XPATH, value = '//*[@class ="PropertyCard__Link"]')
        all_hotel_id = self.driver.find_elements(by = By.XPATH, value = '//*[@data-selenium = "hotel-item"]')
        
        for hotel, hotel_id in zip(all_hotel, all_hotel_id):
            hotel_link = hotel.get_attribute("href")
            self.hotel_list.append(hotel_link)
            self.hotel_id_list.append(hotel_id.get_attribute("data-hotelid"))
```

* Once all the listed hotel's url are collected, a method named `hotel_details` is used to get the following information from each hotel's details page:
  * Unique listing ID
  * Name of the hotel
  * Rating of the hotel
  * The base price per night
  * Hotel's address
  * The associated URL for the hotel
  * All the picture sources 
  * The time the page was scraped
*  Sometimes a deal might have just ended and the associated hotel's page will not show any prices. To overcome this, an `if` statement is used to check 

```go
def hotel_details(self):
        
        hotel_dict_keys = list(self.hotel_dict.keys())
        
        for hotel_number , hotel in enumerate(self.hotel_list):
            individual_hotel_dict = dict.fromkeys(hotel_dict_keys, 0)
            self.driver.get(hotel)
            hotel_page = requests.get(hotel)
            time.sleep(6) 
            
            current_time = self.get_current_time()
            self.hotel_dict["Time Scraped"].append(current_time)
            individual_hotel_dict["Time Scraped"] = current_time
            
            hotel_id = self.hotel_id_list[hotel_number]       
            hotel_name = self.driver.find_element(by = By.XPATH, value = '//*[@data-selenium = "hotel-header-name"]').text
            hotel_rating = self.driver.find_elements(by = By.XPATH, value = '//h3[@class = "Typographystyled__TypographyStyled-sc-j18mtu-0 hTkvyT kite-js-Typography "]')[0].text
            hotel_address = self.driver.find_element(by = By.XPATH, value = '//*[@data-selenium = "hotel-address-map"]').text
            check_hotel_room_avaliability = self.driver.find_elements(by = By.XPATH, value = '//*[@class = "RoomGrid-searchTimeOutText"]')

            if check_hotel_room_avaliability == []:
                hotel_price_per_night = self.driver.find_elements(by = By.XPATH, value = '//*[@class = "Box-sc-kv6pi1-0 hRUYUu StickyNavPrice__priceDetail--lowerText StickyNavPrice__priceDetail--defaultColor"]')
                hotel_price_per_night = hotel_price_per_night[1].text.split(self.currency)[1]
            elif "no rooms" in check_hotel_room_avaliability[0].text:
                hotel_price_per_night = "No rooms avaliable"
            
            hotel_url = self.driver.current_url
            details_list = [hotel_id, hotel_name, hotel_rating, hotel_price_per_night, hotel_address, hotel_url]
            
            for detail, dict_key in zip(details_list, hotel_dict_keys[:7]):
                self.hotel_dict[dict_key].append(detail)
                individual_hotel_dict[dict_key] = detail

        individual_hotel_dict["Hotel Pictures"] = picture_url_list

        time.sleep(5)
```

* To have the `hotel_finder` class run directly when the code is being run, the class is being initialised within the `if __name__ == "__main__"` block.

```go
if __name__ == "__main__":
    destination = "Paris"
    number_of_pages = 3
    start_date = "20/12/2022"
    number_of_nights = 4
    
    all_hotels = hotel_finder(destination,start_date, number_of_nights ,number_of_pages)
    
    print(all_hotels)
```

## __Milestone 4__
* The method named `get_picture` is usd to get all the source of the images posted on the hotel's details page. 

```go
def get_picture(self):
        
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
```

* Once the `get_picture` method has obtained all the sources associated with the images posted on the hotel details' page, a method named `download_pictures` is used to save all the images to the image folder located within each hotel's folder in `raw data`. 

```go
def download_picture(self, picture_url, image_number):
        image_folder_dir = f"{full_path}/images"
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
```

* The information obtained from each hotel's details page is stored in two dictionaries, `self.hotel_dict` and `individual_hotel_dict`.
* The `self.hotel_dict` stores all hotel's information while `individual_hotel_dict` only stores information for the hotel it is currently scrapping and the values of the `individual_hotel_dict` dictionary is set to 0 before storing the next hotel's information. 
* The `individual_hotel_dict` for each corresponding hotel is saved locally in a `data.json` file in the corresponding hotel folder in `raw data` 

```go
def save_data(self,current_hotel_dict):

        if not os.path.exists(full_path):
            os.makedirs(full_path)
        
        with open(f"{full_path}/data.json", "w") as json_file:
            json.dump(current_hotel_dict,json_file)
```

## __Milestone 5__ 