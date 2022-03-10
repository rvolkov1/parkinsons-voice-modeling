from matplotlib import pyplot as plt
import numpy as np
import os

homedir = "C:\\Users\\rossvolkov\\documents\\python\\data"

trials = []
total_patients = len(os.listdir(homedir))
total_over = 0

for patient in os.listdir(homedir):
    num = len(os.listdir(os.path.join(homedir, patient)))
    trials.append(num)
    if (num >= 4): total_over += 1


max_value = np.amax(trials)

print("max value: " + str(max_value))
print("total patients: " + str(total_patients))
print("total over " + str(total_over))

# plt.hist(trials, bins=max_value)
# plt.xlabel('Patient Trials')
# plt.ylabel('Frequency')
# plt.title('Frequency of Amount of Patient Trials')
# plt.xlim(20, max_value)
# plt.ylim(0, 59)
# plt.show()
