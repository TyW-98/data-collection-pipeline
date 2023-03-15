# Data Collection Pipeline
Web scraping has become increasingly popular as businesses and indivudals seek to gather data from websites. This project focuses on developing a web scraper using Python and `Selenium` library for [Agoda.com](https://agoda.com/), a popular hotel booking website. The scraper is designed to automate the process of finding and extracting hotel information from the booking website, making it particularly used for anyone planning a holiday and looking for hotel options in a specific destination. 

The scraper developed is capable of several features, such as data scraping, navigating through the website, selecting the correct destination and dates as well as image scraping. To ensure the reliability of the scraper, a set of unit tests were developed using `unittest` module and the `hypothesis` library. THis helped identify and fix any bugs in the codebase. Additionally, for the scraper to be portable and easy to deploy, the scraper was containersed using Docker, by creating a Docker image from a Dockerfile that includes all the necessary dependencies needed to run the scraper. 

Lastly, a continuous integration and continuous deployment (CI/CD) pipeline were set up to automate the building and pushing of the Docker image to DockerHub whenever there is a push to the main branch of the repository. This ensures that the latest version of the scraper is always available for deployment.

## Dependencies
* Python 3.x
* Selenium
* Chromedriver
* Google Chrome
* Requests

## How to use from GitHub 
To use the hotel finder class, follow the following steps:

1) Clone this repository onto your local machine by running the following commands:
   
   ```bash
   git clone https://github.com/TyW-98/data-collection-pipeline.git
   cd data-collection-pipeline
   ```
2) Install the necessary dependencies using the provided configuration file. Run the following commands:

    ```console
    conda create --name env_name python=3.8
    conda activate env_name
    pip install -r requirements.txt
    ```
3) Download Chromedriver from the [official website](https://sites.google.com/chromium.org/driver/) and add it to your system's path. 
4) Change the values in destination, number_of_hotels, start_date and number_of_nights variable to suit your needs. 
5) Run the hotel finder class by running the following command:

    ```console
    python scraper_class.py
    ```

## How to use from DockerHub
1) Pull the Docker image from DockerHub.

    ```console
    docker pull wey1998/hotel_scraper:latest
    ```
2) Run the Docker image as container.

    ```console
    docker run -d --rm --name hotel_scraper wey1998/hotel_scraper
    ```
3) Check if the container is running.
   
   ```console
   docker ps
   ```
4) Stop the Docker container

    ```console
    docker stop hotel_scraper
    ```
## Contributing
Contributions to this scraper are welcome. Feel free to open a pull request or submit an issue if you have any suggestions or improvements to make.

## **hotel_finder class**

```python
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
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("window-size=1920,1080") 
        self.driver = webdriver.Chrome(options = chrome_options)
        self.driver.get("https://www.agoda.com/") 
        time.sleep(7)
        
        try:
            self.driver.find_elements(by= By.XPATH, value = '//button[@class = "ab-message-button"]')[1].click()   
            time.sleep(2)
        except:
            pass
        
        #self.currency = self.driver.find_element(by = By.XPATH, value = '//p[@class = "Typographystyled__TypographyStyled-sc-j18mtu-0 gSVfcd kite-js-Typography CurrencyContainer__SelectedCurrency__Symbol"]').text
        
    def hotel_location_search(self):
        """Search holiday destination, select holiday dates and filter listings
        
        This function enters the user's holiday destination into the search bar
        ,selects the start and end date of the holiday and filters the listings to show hotels and resorts only.
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
        """Set holiday start and end date

        This function calculates the end date of the holiday using the start date
        of the holiday and the number of nights spent in the hotel then return it in dd/mm/yyyy format.

        Returns:
           dict {str: str}: This dictionary contains the start and end dates of
           the holiday.
        """
        
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
        """Select holiday dates on agoda calender.

        This function selects the booking date on agoda's calender. 

        Args:
            date (str): Hotel booking date in the following format: dd/mm/yyyy
        """
        
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
        """ Select start and end date of booking

        This function uses the set_holiday_dates method to calculate the end date
        of the booking then uses the set_date method to select the start and end 
        date of the booking in agoda's website.
        """
        
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
        """ Gather individual hotel informations   

        This function gets the hotel information from their each respective pages.
        The information includes:
        
        - Hotel's name
        - Unique listing ID
        - Hotel rating
        - Price per night
        - Hotel's address
        - Hotel's page URL
        - Hotel's pictures sources
        - Time scraped. 
        
        To scrape all hotels in the listing pages, the number of hotels must be set to 99 or else the scraper will only scrape the number of hotels defined by the user. 
        
        Returns:
            dict: Contains all the information for each respective hotels
        """
        
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
            
        return individual_hotel_dict 
            
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
    start_date = "15/01/2023"
    number_of_nights = 15
    
    all_hotels = hotel_finder(destination,start_date,number_of_nights,number_of_hotels)
    
    print(all_hotels)
```

## Milestone 1 (Repository Setup)
* Establish a Github repository to version control project files.

## Milestone 2 (Website Selection)
* In order to start the data collection process, the first step is to determine the website from which we want to collect data. For this specific project, Agoda was the chosen website. 

## Milestone 3 (Data Scraping and Navigating through website)
* To scrape data from agoda's website, we need to create a scraper class that contains all the methods necessary for the data collection task. 
* The `hotel_finder` class is initialized with four parameters, the 'holiday_location', 'start_date', 'number_of_nights' and 'number_of_hotels'.
  * `holiday_location` - is the destination where the user wants search for hotels.
  * `start_date` - is the starting date of the holiday period.
  * `number_of_nights` - is the number of nights the user is planning to stay in the hotel.
  * `number_of_hotels` - is the number of hotels the user wants to collect data for. 
  * `hotel_dict` - is also initialized with the keys representing the data that will be collected and empty lists as values, which will be filled in later during the data collection process.
  * `hotel_list` , `hotel_id_list` - initialised as empty lists as they will be used to store the hotel's name and their unique agoda IDs respectively.
  * `working_directory` - this variable is initialised as the directory where the script is currently located by using the `os.path` module to get the current file's directory and replace any backslashes with forward slashes for compatibility with different operating systems.

    ```python
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
    ```
* <font size='3'>**`load_main_page`**</font> - This method loads the home page of agoda's website using chromedriver and closes any ad pop-ups that appear when visiting the site. It also records the selected currency. 

    ```python
    def load_main_page(self):
        """loads the main page of agoda.com

        This function uses selenium webdriver to load the home page of agoda.com.
        After loading agoda's home page it will then try to close the pop up ad
        which always shows up everytime when visiting the page. It will also store
        the default selected currency. 
        """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    self.driver = webdriver.Chrome(options=chrome_options)
    self.driver.get("https://www.agoda.com/") 
    time.sleep(7)
    
    try:
        self.driver.find_elements(by= By.XPATH, value='//button[@class = "ab-message-button"]')[1].click()   
        time.sleep(2)
    except:
        pass
    
    self.currency = self.driver.find_element(by=By.XPATH, value='//p[@class = "Typographystyled__TypographyStyled-sc-j18mtu-0 gSVfcd kite-js-Typography CurrencyContainer__SelectedCurrency__Symbol"]').text
    ```
* <font size='3'>**`hotel_location_search`**</font> - This method enters the holiday destination into the search bar, select the start/end dates by calling the `select_holiday_date` method. Once the dates has been selected, it will then click the search button and filters out all the listings except for hotels and reseorts by toggling their respective checkboxes. 

    ```python
    def hotel_location_search(self):
        """Search holiday destination, select holiday dates and filter listings
        
        This function enters the user's holiday destination into the search bar
        ,selects the start and end date of the holiday and filters the listings to show hotels and resorts only.
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
    ```
* <font size='3'>**`select_holiday_date`**</font> - This method uses the `set_holiday_dates()` to calculate the end date of the booking then uses the `set_dates()` method to select the start and end date of the booking on the website's calender. 

    ```python
    def select_holiday_date(self):
        """ Select start and end date of booking

        This function uses the set_holiday_dates method to calculate the end date
        of the booking then uses the set_date method to select the start and end 
        date of the booking in agoda's website.
        """
        
        holiday_dates = self.set_holiday_dates()
        
        for key_dates in list(holiday_dates.keys()):
            self.set_date(holiday_dates[key_dates])
            time.sleep(5)
    ```

* <font size='3'>**`set_holiday_dates`**</font> - This method calculates the end date of the holiday reservation based on the given start date and the number of nights specified. The resulting end date is stored in the 'holiday_dates' dictionary along with the start date. The dates are formatted as dd/nn/yyyy. This method returns the 'holiday_dates' dictionary as output.

    ```python
    def set_holiday_dates(self):
        """Set holiday start and end date

        This function calculates the end date of the holiday using the start date
        of the holiday and the number of nights spent in the hotel then return it in dd/mm/yyyy format.

        Returns:
           dict {str: str}: This dictionary contains the start and end dates of
           the holiday.
        """
        
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
    ```

* <font size='3'>**`set_date`**</font> - This method uses Selenium to navigate to the Agoda website's calendar and select a specific date. It first extracts all the dates from the calendar, then searches for the element corresponding to the date provided as input. If the date is not found, it clicks on the next button in the calendar to navigate to the next two months. Finally, Chromedriver is used to click on the element corresponding to the date, effectively selecting it.

    ```python
    def set_date(self,date): 
        """Select holiday dates on agoda calender.

        This function selects the booking date on agoda's calender. 

        Args:
            date (str): Hotel booking date in the following format: dd/mm/yyyy
        """
        
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
    ```
* <font size='3'>**`page_scroller`** - This method is used to ensure that all hotel listings are loaded in the dynamically loaded listing page. It achieves this by retrieving the page height, scrolling to the bottom of the page, and checking if the page height has changed. If the page height has changed, the process repeats itself until the page height remains constant. Once the page height is constant, it scrolls to the top of the page.

    ```python
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
    ```

* <font size='3'>**`hotel_listing`**</font> - This method retrieves all the URLs and IDs associated with each hotel listed in the listing page and store them in 'hotel_list' and 'hotel_id_list' respectively.  

    ```python
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
    ```

* <font size='3'>**`hotel_details`**</font> - This method scrapes hotel details for each hotel in the hotel_list obtained from the hotel_listing() method. It visits each hotel page, retrieves the required details such as hotel ID, name, rating, address, price per night, URL, and stores them in the self.hotel_dict dictionary. If the hotel has no rooms available, the hotel_price_per_night is set to "No rooms available". Finally, it then returns the `individual_hotel_dict` dictionary containing the information about the hotel. 

    ```python
    def hotel_details(self):
        """ Gather individual hotel informations   

        This function gets the hotel information from their each respective pages.
        The information includes:
        
        - Hotel's name
        - Unique listing ID
        - Hotel rating
        - Price per night
        - Hotel's address
        - Hotel's page URL
        - Hotel's pictures sources
        - Time scraped. 
        
        To scrape all hotels in the listing pages, the number of hotels must be set to 99 or else the scraper will only scrape the number of hotels defined by the user. 
        
        Returns:
            dict: Contains all the information for each respective hotels
        """
        
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
            
        return individual_hotel_dict 
    ```
* The if \_\_name__ == "\_\_main__": block is used to define the main entry point of a Python program. In this code block, the hotel_finder class is initialized with specific inputs for destination, number_of_pages, start_date, and number_of_nights. Once the all_hotels variable is created by running the hotel_finder class, it is printed to the console using print(all_hotels). This allows the user to see the output of the program when it is executed.

    ```python
    if __name__ == "__main__":
    destination = "Paris"
    number_of_pages = 3
    start_date = "20/12/2022"
    number_of_nights = 4
    
    all_hotels = hotel_finder(destination,start_date, number_of_nights ,number_of_pages)
    
    print(all_hotels)
    ```

## Milestone 4 (Image Scraping)
* <font size='3'>__`get_picture`__ </font> - This method retrieves the URLs of all the pictures posted on the hotel's information page and stores them in a list. This is done by first clicking on the "see all pictures" button to load all the pictures, then retrieves the URLs of the pictures and appends them to the list. The 'download_picture' method is then called to download each picture. The list of picture URLs is added to the 'hotel_dict' dictionary as well. 

    ```python
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
    ```
* <font size="3">__`download_picture`__</font> - This method downloads the hotel picture from the provided URL and saves it in the directory associated with the hotel. Each image is renamed according to the following format: "<current_date>_<current_time>_<image_number>.png". If the image folder already exists, it will first delete it before creating a new one. This method uses the `requests` module to get image data from the provided URL. 

    ```python
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
    ```

* <font size="3">**`save_data`**</font> - This method saves the information dictionary it receives and saves it to a JSON file named "data.json" locally in the corresponding hotel directory. 

    ```python
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
    ```

## Milestone 5 (Unit Testing)
* Developed unit tests for the hotel scraper class `hotel_finder`. It tests three of the class's methods, `get_current_time()`,`file_path()` and `individual_hotel_dict()`.
  * <font size="3">`test_get_current_time()`</font> - This method tests if the `get_current_time()` method return the current time as expected and in the correct format.
  * <font size="3">`test_file_path()`</font> - This method tests if the `file_path()` method returns the correct file path given a hotel ID.
  * <font size="3">`test_individual_hotel_dict()`</font> - This method tests if the `individual_hotel_dict()` dictionary is correctly initialized with the expected keys.
* The `hypothesis` library is used to generate test inputs for the `test_file_path()` method. Once all the test are completed, the `teardown()` method is called to clean up the resources used by the test cases. 
  

    ```python
    from scraper_class import hotel_finder
from hypothesis import given
import hypothesis.strategies as st
import unittest
import datetime
import os


class hotelfinderTestCase(unittest.TestCase):
    
    def setUp(self):
        
        self.hotel = hotel_finder("Penang","25/12/2022",4,1)
        
    def test_get_current_time(self):
        expected_value = datetime.datetime.now().replace(microsecond=0).isoformat()
        actual_value = self.hotel.get_current_time()
        self.assertAlmostEqual(expected_value,actual_value)
    
    @given(st.integers().filter(lambda x : x >100000 and x < 1000000))
    def test_file_path(self, n):
        working_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
        folder_name = f"Test Hotel (hotel ID - {n})"
        expected_value = f"{working_dir}/raw data/Penang/{folder_name}"
        actual_value = self.hotel.file_path("Test Hotel",n)
        self.assertEqual(expected_value,actual_value)
        
    def test_individual_hotel_dict(self):
        expected_value = [
            "Hotel ID",
            "Hotel Name",
            "Hotel Rating",
            "Price/Night",
            "Address",
            "Hotel URL",
            "Hotel Pictures",
            "Time Scraped"
        ]
        expected_datatype = [
            int,
            str,
            float,
            float,
            str,
            str,
            list,
            str,
        ]
        actual_value = list(self.hotel.hotel_dict.keys())
        actual_datatypes = list(self.hotel.hotel_dict.values())
        self.assertListEqual(expected_value,actual_value)
        
        for n, actual_datatype in enumerate(actual_datatypes):
            self.assertEqual(expected_datatype[n], type(actual_datatype[0]))
            self.assertNotEqual([],actual_datatype[0])
        
    def tearDown(self):
        
        del self.hotel
    ```

## Milestone 6 (Containerising Scraper)
* To containerise the scraper to run it virtually, the `load_main_page()` method needs to be modified to run the scraper in headless mode. 

    ```python
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
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("window-size=1920,1080") 
        self.driver = webdriver.Chrome(options = chrome_options)
        self.driver.get("https://www.agoda.com/") 
        time.sleep(7)
        
        try:
            self.driver.find_elements(by= By.XPATH, value = '//button[@class = "ab-message-button"]')[1].click()   
            time.sleep(2)
        except:
            pass
    ```

* Create a Dockerfile to define the Docker image
  
    ```
    FROM python:latest

    # Installing Google Chrome
    RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
    RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
    RUN apt-get -y update
    RUN apt-get install -y google-chrome-stable

    # Installing Chromedriver
    RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
    RUN apt-get install -yqq unzip
    RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

    ENV PORT 5432

    COPY . .

    RUN pip install selenium

    RUN pip install requests

    CMD ["python","scraper_class.py"]
    ```

* Build the Docker image from Dockerfile

    ```console
    docker build -t hotel_scraper .
    ```

* Run the Docker container
  
    ```console
    docker run -d --rm --name hotel_scraper hotel_scraper
    ```

* Push Docker image to DockerHub

    ```console
    docker tag hotel_scraper:latest wey1998/hotel_scraper:latest
    docker push wey1998/hotel_scraper:latest
    ```

## Milestone 7 (Setup CI/CD pipeline for Docker image)
* Set up GitHub secrets to securely store Docker login details, including DockerHub username and password or token.
* Create a Github action to automatially build and push Docker image to DockerHub when there is a push to main branch of repository.

    ```yaml
    name: Data collection pipeline automatically push to docker

    on:
    push:
        branches: [main]

    jobs:
    build:

        runs-on: ubuntu-latest

        steps:

        - uses: actions/checkout@v3

        - name: Setup python 3.8
        uses: actions/setup-python@v4
        with:
            python-version: '3.8'

        - name: Setup docker QEMU
        uses: docker/setup-qemu-action@v2

        - name: Setup docker Buildx
        uses: docker/setup-buildx-action@v2

        - name: Login to DockerHub
        uses: docker/login-action@v2
        with:
            username: ${{ secrets.DOCKER_USERNAME}}
            password: ${{ secrets.DOCKER_PASSWORD}}

        - name: Build and push image
        uses: docker/build-push-action@v3
        with:
            context: .
            push: true
            tags: wey1998/hotel_scraper:latest    
    ```

## Conclusion
In this project, a web scraper was developed using Python and Selenium. The web scraper can navigates through the hotel booking website, extract information of the hotels and save it to a JSON file. It is also able to scrape images of the hotel and save them locally. To ensure the reliability of the code, a set of unit tests were developed using `unittest` module and `hypothesis` library.  This helped us identify and fix any bugs in the codebase. 

In order for the scraper to be portable and easy to deploy, the scraper was containerised using Docker. This is done by creating a Dockerfile to build a Docker image that includes all the dependencies needed to run the scraper. Lastly, a continous integration and continous deployment (CI/CD) pipeline that automatically builds and push the Docker image to DockerHub whenever there is a push to the main branch of the repository was setup, where the Docker login details are securely stored using Github Secrets. 

Overall, this project provided us with valuable experience in web scraping, image scraping, unit testing, Docker and CI/CD pipelines.