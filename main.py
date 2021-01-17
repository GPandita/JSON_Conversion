"""
Created on Sat Jan 16

@author: Gaurav Pandita
"""

import csv
import json
import sys

def read_json_file(input_file_path):
    try:
        with open(input_file_path, "r") as read_file:
            data = json.load(read_file)
        print("\n**** Read JSON file " + input_file_path + " ****\n")
        return data
    except:
        print("\n---- Error while reading the json file. Please check the input file ----\n")
        sys.exit()

def transform_to_frame_wise(data):
    try:
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
        return data
    except:
        print("\n---- Error while transforming the json. Please verify the input json file ----\n")
        sys.exit()

def write_json_file(data):
    try:
        with open("output/output.json", "w") as outfile_json:
            json.dump(data, outfile_json)
        outfile_json.close()
        print("\n**** Transformed JSON file. Written to output directory as output.json ****\n")
    except:
        print("\n---- Error while writing output json file. Please check if output directory exists ----\n")
        sys.exit()

def generate_csv_file(data):
    try:
        with open("output/output.csv", "w") as outfile_csv:
            writer = csv.writer(outfile_csv)
            writer.writerow(["frame_id", "tracking_id", "label"])
            for tracker in data['answer_key']['video2d']['data']['trackers']:
                for frame in tracker['frames']:
                    writer.writerow([frame, tracker['_id'], tracker['frames'][frame]["label"]])
        outfile_csv.close()
        print("\n**** CSV file generated. Written to output directory as output.csv ****\n")
    except:
        print("\n---- Error while writing output csv file. Please check if output directory exists ----\n")
        sys.exit()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nRun the file as : [python] main.py [input_json_file_path]\n")
    else:
        data = read_json_file(sys.argv[1])
        generate_csv_file(data)
        data = transform_to_frame_wise(data)
        write_json_file(data)
        data.clear()
        print("\n**** Successful ****\n")