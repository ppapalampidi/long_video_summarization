import os
import glob
import json

all_information = glob.glob("videos/*.json")

for info in all_information:
    filename = "summaries" + info[6:]
    if os.path.exists(filename):
        obj = json.load(open(filename))
    else:
        obj = {}

    info_obj = json.load(open(info))

    if "description" in info_obj:
        if len(
        #to finish this off, somehow identify if the description is a summary, if it is, add it to the obj, then write the obj
