from scraper_class import hotel_finder
from hypothesis import given
from selenium import webdriver
import hypothesis.strategies as st
import unittest
import time
import datetime
import os


class hotelfinderTestCase(unittest.TestCase):
    
    def setUp(self):
        
        self.hotel = hotel_finder("Penang","25/12/2022",4,1)
        
    def test_get_current_time(self):
        expected_value = datetime.datetime.now().replace(microsecond=0).isoformat()
        actual_value = self.hotel.get_current_time()
        self.assertAlmostEqual(expected_value,actual_value)
        
    def test_file_path(self):
        working_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
        folder_name = "Test Hotel (hotel ID - 122)"
        expected_value = f"{working_dir}/raw data/Penang/{folder_name}"
        actual_value = self.hotel.file_path("Test Hotel",122)
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
        
    def tearDown(self):
        
        del self.hotel
        
if __name__ == "__main__":    
    unittest.main(argv = [""],  verbosity = 3, exit=False)