import csv
import os

# 1 is positive 0 is negative
homedir = "C:\\Users\\rossvolkov\\documents\\python\\data"

# total 65000
NUM_OF_PATIENTS = 65000

patient_blacklist = {}
patient_indices = {}

def splice_rows(d_row, num, i_row, diagnosis):
    return [d_row[3]] + [num] + d_row[7:] + i_row[7:] + [diagnosis]

def validate_patient(row):
    if (row[4] == "true" or row[25] == "true"):
        # discard patient
        return -1
    elif (row[5] != "" and row[21] == "true"):
        #patient is positive
        return 1
    elif (row[5] == "" and row[21] == "false"):
        #negative
        return 0
    else:
        #discard patient
        return -1

def validate_trial(row, diagnosis):
    print(diagnosis)
    if (diagnosis == 0 and row[-2] == "I don't take Parkinson medications"):
        return True
    elif (diagnosis == 1 and (row[-2] == "Another time" or row[-2] == "Immediately before Parkinson medication")):
        return True
    else:
        return False

with open("patient_demographics.csv", 'r') as demographics, open("voice_identifiers.csv", 'r') as identifiers, open("filtered_dataset.csv", 'w+') as data, open("unfit_data.csv", "w+") as unfit_data:
    demographics_reader = csv.reader(demographics, delimiter=',')
    identifiers_reader = csv.reader(identifiers, delimiter=',')
    data_writer = csv.writer(data, delimiter=",")
    unfit_writer = csv.writer(unfit_data, delimiter=",")

    d_header = next(demographics_reader)
    i_header = next(identifiers_reader)
    spliced_rows = splice_rows(d_header, "num of trials", i_header, "diagnosis")
    data_writer.writerow(spliced_rows)
    unfit_writer.writerow(spliced_rows)

    i = 0
    for i_row in identifiers_reader:
        print("loop number :" + str(i))
        i+= 1
        if (i >= NUM_OF_PATIENTS): break
        demographics.seek(0)
        newreader = csv.reader(demographics)
        patient_id = i_row[3]

        if patient_id in patient_blacklist:
            print("blacklist")
            unfit_writer.writerow(["blacklist"])
            continue
        if patient_id not in patient_indices:
            for r in newreader:
                if r[3] == patient_id:
                    patient_indices[patient_id] = r + [3]
            if patient_id not in patient_indices:
                unfit_writer.writerow(["skipped"])
                print("skipped " + patient_id)
                continue

        d_row = patient_indices[patient_id]
        row_values = splice_rows(d_row, [len(os.listdir(os.path.join(homedir, str(patient_id))))], i_row, patient_indices[patient_id][-1])

        if (row_values[-1] == 3):
            diagnosis = validate_patient(row_values)
            row_values[-1] = patient_indices[patient_id][-1] = diagnosis
            if(diagnosis == -1):
                patient_blacklist[patient_id] = 1
                unfit_writer.writerow(row_values)
                print("unfit")
                continue

        if (not validate_trial(row_values, patient_indices[patient_id][-1])):
            unfit_writer.writerow(row_values)
            print("trial unfit")
            continue

        #print('valid patient and trial')
        data_writer.writerow(row_values)
