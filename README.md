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

* Create a `hotel_location_search` method to 