# Author: Gaurav Pandita
# Created On : 16 January 2021
# Python 3
import json
import csv

# fetch input file path and output directory from paths.json
with open("paths.json", "r") as config_file:
    data = json.load(config_file)
    input_file_path = data['input_file_path']
    outfile_directory = data['output_directory']
    config_file.close()

# opening tracker_wise.json
with open(input_file_path, "r") as read_file:
    data = json.load(read_file)

# creating a new dictionary for creating frame_wise json
new_data = {"answer_key":{"video2d":{"data":{"frames":{}}}}}

# opeing output.csv for filling in ["frame_id", "tracking_id", "label"] 
with open(outfile_directory + "output.csv", "w") as outfile_csv:
    # creating a csv_writer for writing to csv file
    writer = csv.writer(outfile_csv)
    writer.writerow(["frame_id", "tracking_id", "label"])

    # iterating over every tracker
    for tracker in data['answer_key']['video2d']['data']['trackers']:
        # iterating over every frame
        for frame in tracker['frames']:
            if frame not in new_data['answer_key']['video2d']['data']['frames'].keys():
                new_data['answer_key']['video2d']['data']['frames'][frame] = []
            # creating a dictionary with tracker_id as key (first key in the frame_wise json)
            d = {'tracker_id':tracker['_id']}
            # appending the tracker_id dictionary to the frames list
            new_data['answer_key']['video2d']['data']['frames'][frame].append(d)
            # adding all other elements to lastly added dictionary to the frame list as it is (as they don`t need to be modified)
            new_data['answer_key']['video2d']['data']['frames'][frame][-1].update(**tracker['frames'][frame])
            new_data['answer_key']['video2d']['data']['frames'][frame][-1]['color'] = tracker['color']
            # write out tracker_id, frame_id and label to csv file
            writer.writerow([frame, tracker['_id'], tracker['frames'][frame]["label"]])

    read_file.close()

# opening output.json file in output directory to write out frame_wise json
with open(outfile_directory + "output.json", "w") as outfile_json:
    # converting dict to json format
    json.dump(new_data, outfile_json)
    outfile_json.close()

# clearing out used dictionaries
data.clear()
new_data.clear()