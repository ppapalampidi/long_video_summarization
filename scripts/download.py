import pytube
import json
import glob
import os
import multiprocessing as mp
from argparse import ArgumentParser
from itertools import repeat


def is_integer(string):
    try:
        int(string)
        return True
    except:
        return False


def transcript_to_list(captions):
    line_index = 0
    in_line = False
    current_line = ["", ""]
    lines = []
    for item in captions:
        if is_integer(item):
            in_line = True
            line_index = 0
            current_line = ["", ""]
            continue
        if in_line:
            current_line[line_index] = item
            if line_index == 1:
                in_line = False
                line_index = 0
                lines.append(current_line)
                continue
            line_index += 1
    return lines


def download_video(episode_information, output_dir, verbose=False):
    if verbose:
        print("Downloading: " + episode_information[0]["url"])
    vid = pytube.YouTube(episode_information[0]["url"])
    if vid.length < 15*60:
        if verbose:
            print("Video is too short to be a full episode")

    if os.path.exists(os.path.join(output_dir, episode_information[1]+".json")):
        if verbose:
            print("Video information already exists")
    else:
        information = {}
        information["description"] = vid.description
        captions = vid.captions
        # get captions
        if "en" in captions:
            information["captions"] = transcript_to_list(
                captions["en"].generate_srt_captions().split("\n"))
        elif "a.en" in captions:
            information["captions"] = transcript_to_list(
                captions["a.en"].generate_srt_captions().split("\n"))
        else:
            if verbose:
                print("No captions found for video: ", episode_information[1])
        with open(os.path.join(output_dir, episode_information[1]+".json"), 'w') as outfile:
            json.dump(information, outfile, indent=4)

    if os.path.exists(os.path.join(output_dir, episode_information[1]+".mp4")):
        if verbose:
            print("Video already exists")
        return
    streams = vid.streams.filter(
        file_extension='mp4', progressive=True).order_by('resolution').desc()
    downloaded = False
    if len(streams) == 0:
        if verbose:
            print("No streams found")
    for stream in streams:
        if stream.resolution == '1080p':
            continue
        else:
            stream.download(output_dir, filename=episode_information[1]+".mp4")
            downloaded = True
            break
    if not downloaded:
        if verbose:
            print("No suitable video found")
    if verbose:
        print("Downloaded: " + episode_information[1])


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--input_directory", type=str,
                            help="Input directory of json files containing transcripts with URLs")
    arg_parser.add_argument("--output_directory", type=str,
                            help="Output directory to store json and mp4 files")
    arg_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose output")
    args = arg_parser.parse_args()

    input_dir = args.input_directory
    output_dir = args.output_directory
    verbose = args.verbose

    all_episodes = glob.glob(input_dir + "/*")
    zipped_episodes = [(json.load(open(file)), file[12:-5])
                       for file in all_episodes]

    breakpoint()
    with mp.Pool(mp.cpu_count()) as p:
        p.starmap(download_video, zip(zipped_episodes,
                  repeat(output_dir), repeat(verbose)))
