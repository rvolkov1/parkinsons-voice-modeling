import os, shutil, csv

location = "C:\\Users\\rossvolkov\\.synapseCache"
dest = "C:\\Users\\rossvolkov\\documents\\python\\data"

identifiers = {}

with open('voice_identifiers.csv') as f:
    reader = csv.reader(f, delimiter=",")
    i = 0
    for row in reader:
        identifiers[row[7]] = [row[3], i]
        identifiers[row[8]] = [row[3], i]
        i += 1

for container in os.listdir(location):
    container = os.path.join(location, container)
    for directory in os.listdir(container):
        directory = os.path.join(container, directory)

        file = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.tmp')]

        if (len(file) > 0):
            if "audio_audio" in file[0]:
                num = os.path.basename(directory)
                if num in identifiers:
                    patient_id = identifiers[num][0]
                    row = identifiers[num][1]

                    destination = dest + "\\" + patient_id + "\\" + str(row)

                    if not os.path.isdir(destination):
                        os.makedirs(destination)
                    shutil.copy(os.path.join(directory, file[0]), destination + "\\" + num + "_audio.m4a")
            elif "audio_countdown" in file[0]:
                num = os.path.basename(directory)
                if num in identifiers:
                    patient_id = identifiers[num][0]
                    row = identifiers[num][1]

                    destination = dest + "\\" + patient_id + "\\" + str(row)

                    if not os.path.isdir(destination):
                        os.makedirs(destination)

                    shutil.copy(os.path.join(directory, file[0]), destination + "\\" + num + "_countdown.m4a")
