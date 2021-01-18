"""
Created on Sat Jan 16
@author: Gaurav Panditad
"""

import csv
import json
import logging
import os
import sys


def read_json_file(input_file_path):
    with open(input_file_path, "r") as read_file:
        data = json.load(read_file)
    logging.info("Read Input JSON (" + input_file_path + ") - SUCCESS")
    return data


def transform_to_frame_wise(data):
    # data_ptr is like a pointer referencing data dictionary
    data_ptr = data['answer_key']['video2d']['data']
    # creating frames entry in data dictionary for adding frame_wise data
    data_ptr['frames'] = {}

    # iterating over every tracker entry
    for tracker in data_ptr['trackers']:
        # iterating over every frame in a tracker
        for frame in tracker['frames']:
            # if first entry for a frame
            if frame not in data_ptr['frames'].keys():
                data_ptr['frames'][frame] = []
                
            data_ptr['frames'][frame].append({'tracker_id':tracker['_id']})
            data_ptr['frames'][frame][-1].update(**tracker['frames'][frame])
            data_ptr['frames'][frame][-1]['color'] = tracker['color']

    # remove tracker_wise data
    del data_ptr['trackers']
    logging.info("Transform JSON - SUCCESS")
    return data


def write_json_file(data):
    # if output directory doesn't exists then create one
    if not os.path.exists('output'):
        os.makedirs('output')
    with open("output/output.json", "w") as outfile_json:
        json.dump(data, outfile_json)
    outfile_json.close()
    logging.info("JSON File Write - SUCCESS (output/output.json)")


def generate_csv_file(data):
    if not os.path.exists('output'):
        os.makedirs('output')
    with open("output/output.csv", "w") as outfile_csv:
        writer = csv.writer(outfile_csv)
        writer.writerow(["frame_id", "tracking_id", "label"])
        for tracker in data['answer_key']['video2d']['data']['trackers']:
            for frame in tracker['frames']:
                writer.writerow([frame, tracker['_id'], tracker['frames'][frame]["label"]])
    outfile_csv.close()
    logging.info("CSV Generate & Wirte - SUCCESS (output/output.csv)")


if __name__ == "__main__":
    # if logs directory doesn't exist then create one
    if not os.path.exists('logs'):
        os.makedirs('logs')
    # setting logging configuration
    logging.basicConfig(filename="logs/main.log", level=logging.INFO, format='%(asctime)s - %(process)d - %(levelname)s  \t- %(message)s')

    if len(sys.argv) != 2:
        print("Run as : [python] main.py [input_json_file_path]")
        sys.exit()
    try:
        logging.info("**** STARTING ****")
        data = read_json_file(sys.argv[1])
        generate_csv_file(data)
        data = transform_to_frame_wise(data)
        write_json_file(data)
        data.clear()
        print("**** SUCCESSFUL ****")
        logging.info("**** SUCCESSFUL ****")
    except Exception as error:
        exception_message = str(error)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        logging.error(f"{exception_message} - {exception_type} - Line {exception_traceback.tb_lineno}")
        logging.info("**** UNSUCCESSFUL ****")
        print("**** UNSUCCESSFUL (For more information check logs/main.log) ****")
else:
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(filename="logs/test.log", level=logging.INFO, format='%(asctime)s - %(process)d - %(levelname)s  \t- %(message)s')