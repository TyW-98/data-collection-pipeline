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