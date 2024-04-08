import glob
import json
import os

transcript_files = os.listdir("transcripts")
summary_files = os.listdir("summaries")

transcripts = [json.load(open("transcripts/" + f)) for f in transcript_files]
summaries = [json.load(open("summaries/" + f)) for f in summary_files]

for filename, transcript in zip(transcript_files, transcripts):
    if os.path.exists("summaries/" + filename):
        obj = json.load(open("summaries/" + filename))
    else:
        obj = {}

    if "Recap" in transcript:
        if len(transcript["Recap"]) > 0:
            if len(" ".join(transcript["Recap"]).split(" ")) > 6:
                obj["tvmega_recap"] = " ".join(transcript["Recap"])
    if "Episode Summary" in transcript:
        if len(transcript["Episode Summary"]) > 0:
            if len(" ".join(transcript["Episode Summary"]).split(" ")) > 6:
                obj["tvmega_summary"] = " ".join(transcript["Episode Summary"])

    with open("temp_summaries/" + filename, "w") as f:
        json.dump(obj, f, indent=4)

