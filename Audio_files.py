# import needed modules
import json
import random

# establish empty arr of sound files
file_list = []

with open('Sound.json') as f:
    file_list = json.load(f)

def rand_sound(f=file_list):
    return (random.choice(f["audio_files"]))


