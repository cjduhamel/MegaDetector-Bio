import os
import subprocess
import json
import shutil

script_to_run = "megaDetect.py"
model = "MDV5A"
input_folder = "F:/Original Files"
output_file = "./output.json"
destinationFolder = "./photos/resultPhotosCopy"
dest_folder_hanna = "F:/pruned_dir_tree"

        
subprocess.run(["python", script_to_run, model, input_folder, output_file, "--recursive"], check=True)

data = None
detected_paths = []

with open(output_file, "r") as f:
    data = json.load(f)

for photo in data["images"]:
    if len(photo["detections"]) > 0:
        for detection in photo["detections"]:
            if detection["conf"] >= 0.4:
                detected_paths.append(photo["file"])
                newdest = photo["file"].replace(input_folder, dest_folder_hanna)
                newdest = os.path.dirname(newdest)
                if not os.path.exists(newdest):
                    os.makedirs(newdest)
                shutil.copy(photo["file"], newdest)
                print("Copied " + photo["file"] + " to " + newdest)
                break;

 



