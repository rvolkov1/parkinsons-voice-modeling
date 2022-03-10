import csv

num_pd_patients = 0
total_patients = 0

num_pd_trials = 0
total_trials = 0

past_patients = {}

with open("C:\\Users\\rossvolkov\\Documents\\python\\sheets\\features.csv", newline='\n') as data:
    data_reader = csv.reader(data, delimiter=',')

    # skip header
    next(data_reader)

    for row in data_reader:
        diagnosis = int(row[3])
        if diagnosis != 1 and diagnosis != 0: print("error")

        num_pd_trials += diagnosis

        patient_id = row[0]

        if patient_id not in past_patients:
            past_patients[patient_id] = []

            num_pd_patients += diagnosis
            total_patients += 1

        total_trials += 1
        past_patients[patient_id] = past_patients[patient_id] + [total_trials]

with open("C:\\Users\\rossvolkov\\Documents\\python\\sheets\\trials_by_patient.csv", "w") as trials_dataset:
    trials_writer = csv.writer(trials_dataset, delimiter=',')

    for patient, trials in past_patients.items():
        trials.insert(0, patient)
        trials_writer.writerow(trials)


print ("PD patients: " + str(num_pd_patients))
print ("Control patients: " + str(total_patients - num_pd_patients))
print ("Total patients: " + str(total_patients))
print("\n")
print ("PD trials: " + str(num_pd_trials))
print ("Control trials: " + str(total_trials - num_pd_trials))
print ("Total trials: " + str(total_trials))
