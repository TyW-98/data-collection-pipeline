from scraper_class import hotel_finder
from hypothesis import given
from selenium import webdriver
import hypothesis.strategies as st
import unittest
import time
import datetime


class hotelfinderTestCase(unittest.TestCase):
    
    def setUp(self):
        
        self.hotel = hotel_finder("Penang","25/12/2022",4,1)
        
    def test_get_current_time(self):
        expected_value = datetime.datetime.now().replace(microsecond=0).isoformat()
        actual_value = self.hotel.get_current_time()
        self.assertAlmostEqual(expected_value,actual_value)
        
    def test_load_home_page(self):
        expected_value = "https://www.agoda.com/"
        actual_value = self.hotel.load_main_page().getCurrentUrl()
        self.assertEqual(expected_value,actual_value)
        
    def tearDown(self):
        
        del self.hotel
        
if __name__ == "__main__":    
    unittest.main(argv = [""],  verbosity = 2, exit=False)