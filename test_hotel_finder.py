from scraper_class import hotel_finder
from hypothesis import given
from selenium import webdriver
import hypothesis.strategies as st
import unittest
import time
import datetime


class hotelfinderTestCase(unittest.TestCase):
    
    def setUp(self):
        
        self.hotel = hotel_finder("Penang","25/12/2022",4,4)
        self.driver = webdriver.Chrome()
        
    def test_get_current_time(self):
        expected_value = datetime.datetime.now().replace(microsecond=0).isoformat()
        actual_value = self.hotel.get_current_time()
        self.assertAlmostEqual(expected_value,actual_value)
        
if __name__ == "__main__":    
    unittest.main(argv = [""],  verbosity = 2, exit=False)