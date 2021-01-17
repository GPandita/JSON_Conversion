import csv
import json
import sys

def read_json_file(input_file_path):
    with open(input_file_path, "r") as read_file:
        data = json.load(read_file)
    print("\n**** Successfully read JSON file ****\n")
    return data

def transform_to_frame_wise(data):
    temp = data['answer_key']['video2d']['data']
    temp['frames'] = {}

    for tracker in temp['trackers']:
        for frame in tracker['frames']:
            if frame not in temp['frames'].keys():
                temp['frames'][frame] = []
            d = {'tracker_id':tracker['_id']}
            temp['frames'][frame].append(d)
            temp['frames'][frame][-1].update(**tracker['frames'][frame])
            temp['frames'][frame][-1]['color'] = tracker['color']

    del temp['trackers']
    return data

def write_json_file(data):
    with open("output/output1.json", "w") as outfile_json:
        json.dump(data, outfile_json)
    outfile_json.close()
    print("\n**** Transformed JSON file. Written to output directory as output.json ****\n")

def generate_csv_file(data):
    with open("output/output1.csv", "w") as outfile_csv:
#        writer = csv.writer(outfile_csv)
#        writer.writerow(["frame_id", "tracking_id", "label"])
        temp = data['answer_key']['video2d']['data']
        for frames in temp['frames']:
            for frame in frames:
                continue
#                print(frame)
#        writer.writerow([frame, tracker['_id'], tracker['frames'][frame]["label"]])

if __name__ == "__main__":
    data = read_json_file(sys.argv[1])
    data = transform_to_frame_wise(data)
    write_json_file(data)
    generate_csv_file(data)