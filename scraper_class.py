import requests 
import time
from bs4 import BeautifulSoup


main_page = requests.get("https://www.agoda.com/?cid=1844104")