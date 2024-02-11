# import needed modules
import json
import random
file_list = []

with open('Sound.json') as f:
    file_list = json.load(f)
    print(file_list["audio_files"][1])

