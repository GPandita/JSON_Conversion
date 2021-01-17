"""
Created on Sat Jan 17

@author: Gaurav Pandita
"""
import unittest
from main import *

class TestJsonConversion(unittest.TestCase):
    def test_transform(self):
        # input file in test drectory
        input_data = read_json_file("test/input_test.json")
        # transformed output
        output_data = transform_to_frame_wise(input_data)
        # known correct test case output
        original_output_data = read_json_file("test/output_test.json")
        self.assertDictEqual(output_data, original_output_data)

if __name__ == "__main__":
    unittest.main()