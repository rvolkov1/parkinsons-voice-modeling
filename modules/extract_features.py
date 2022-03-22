import opensmile
from pydub import AudioSegment
import librosa

import pandas as pd
import glob
import csv
import os

loc = "C:\\Users\\rossvolkov\\documents\\python\\data\\"
filename = "../sheets/LLD_dataset.csv"

smile = opensmile.Smile(
    feature_set = opensmile.FeatureSet.eGeMAPSv02,
    feature_level = opensmile.FeatureLevel.LowLevelDescriptors,
    num_workers = 6
)

#y = smile.process_file("C:\\Users\\rossvolkov\\documents\\python\\data\\00a78d55-a227-4944-b6e2-a8a8f9034f24\\3670\\5515906_audio.m4a")

def splice_rows(d_row, f_row):
    return [d_row[0]] + d_row[-4:-2] + [d_row[-1]] + f_row[0:900]

def audio_converter(m4a_file):
    index = m4a_file.index(".")
    wav_file = m4a_file[0:index] + ".wav"

    try:
        track = AudioSegment.from_file(m4a_file,  format= 'm4a')
    except:
        return 1

    file_handle = track.export(wav_file, format='wav')
    return wav_file

with open('../sheets/filtered_dataset.csv', newline='\n') as dataset, open(filename, 'w', newline="") as features:
    data_reader = csv.reader(dataset, delimiter=',')
    features_writer = csv.writer(features, delimiter=",")

    data_header = next(data_reader)
    features_header = smile.feature_names
    features_writer.writerow(splice_rows(data_header, features_header))

    for i, row in enumerate(data_reader):
        print("loop number: " +  str(i))

        patient_id = row[0]
        audio = row[29]

        #change depending on file input
        file = audio_converter(glob.glob(loc + patient_id + "\\**\\" + audio + "_audio.m4a")[0])

        # try:
        #     file = glob.glob(loc + patient_id + "\\**\\*.wav")[0]
        # except:
        #     continue

        #forgot why this is here
        if file == 1: continue
        y = smile.process_file(file)
        y_list = y.values.tolist()
        for j, y_row in enumerate(y_list):
            features_writer.writerow(splice_rows(row, y_row))
            if (j == 900): break
        #if (i >= 20): break
