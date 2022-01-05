import os
import glob
import argparse
from pydub.silence import split_on_silence
from pydub import AudioSegment

root_folder = "data"
merged_filename = None


def merge_wavs(recordings_folder):
    global merged_filename
    list_of_wavs = sorted(glob.glob(recordings_folder+"/*"))

    wavfiles = " ".join(list_of_wavs)
    command = "sox " + wavfiles + " " + merged_filename
    os.system(command)

def remove_folder_and_content(path):
    if not os.path.exists(path):
        return False

    for file in os.listdir(path):
        try:
            os.remove(os.path.join(path, file))
        except IsADirectoryError:
            os.rmdir(os.path.join(path, file))
    os.rmdir(path)

def split_wavs(current_folder):
    global merged_filename
    data = AudioSegment.from_wav(merged_filename)
    chunks = split_on_silence(data, min_silence_len=500, silence_thresh=-48, keep_silence=100)

    for i in range(0, len(chunks)):
        save_path = os.path.join(current_folder, "track_"+str(i+1)+".wav")
        chunks[i].export(save_path, format="wav")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Merge partitioned recorded wav files and split by silence after.')
    parser.add_argument('--recordings', metavar='2022-01-05T10-06-39Z/', required=True, type=str,
            help='The folder where the partitioned wav files to be joined are stored.')
    parser.add_argument('--keep', action='store_true',
            help="Don't delete the original recordings and the merged file.")
    args = parser.parse_args()
    folder = args.recordings
    recordings_folder = os.path.join("recordings", folder)
    current_folder = os.path.join(root_folder, folder)

    try:
        os.makedirs(current_folder)
    except OSError:
        print("Folder already exists.")

    merged_filename = os.path.join(root_folder, folder) + ".wav"
    merge_wavs(recordings_folder)
    split_wavs(current_folder)
    if not args.keep:
        remove_folder_and_content(recordings_folder)
        os.remove(merged_filename)