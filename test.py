"""
Created on Sat Jan 17
@author: Gaurav Pandita
"""

import logging
import sys
import unittest
from main import read_json_file, transform_to_frame_wise


class TestJsonConversion(unittest.TestCase):
    def test_transform(self):
        try:
            # input file in test drectory
            input_data = read_json_file("test/input_test.json")
            # transformed output
            output_data = transform_to_frame_wise(input_data)
            # known correct test case output
            original_output_data = read_json_file("test/output_test.json")
            self.assertDictEqual(output_data, original_output_data)
        except Exception as error:
            exception_message = str(error)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            logging.error(f"{exception_message} - {exception_type} - Line {exception_traceback.tb_lineno}")
            logging.error("**** TEST CASE - test_transform - Fail ****")
            raise error
        logging.info("**** TEST CASE - test_transform - Pass ****")


if __name__ == "__main__":
    logging.info("**** TEST START ****")
    unittest.main()