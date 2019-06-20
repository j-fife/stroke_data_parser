import random
import csv
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from sklearn import svm

with open("actigraph_reads/DW-001-both_merged.csv") as pat_01: csv_1_list = list(csv.reader(pat_01, delimiter=","))
with open("actigraph_reads/DW-002-both_merged.csv") as pat_02: csv_2_list = list(csv.reader(pat_02, delimiter=","))
with open("actigraph_reads/DW-003-both_merged.csv") as pat_03: csv_3_list = list(csv.reader(pat_03, delimiter=","))
with open("actigraph_reads/DW-004-both_merged.csv") as pat_04: csv_4_list = list(csv.reader(pat_04, delimiter=","))
with open("actigraph_reads/DW-005-both_merged.csv") as pat_05: csv_5_list = list(csv.reader(pat_05, delimiter=","))
with open("actigraph_reads/DW-006-both_merged.csv") as pat_06: csv_6_list = list(csv.reader(pat_06, delimiter=","))
with open("actigraph_reads/DW-007-both_merged.csv") as pat_07: csv_7_list = list(csv.reader(pat_07, delimiter=","))
#with open("actigraph_reads/DW-008-both_merged.csv") as pat_08: csv_8_list = list(csv.reader(pat_08, delimiter=","))
csv_file_list = [csv_1_list, csv_2_list, csv_3_list, csv_4_list, csv_5_list, csv_6_list, csv_7_list]
labelsDict = {
    1 : [1,1,1,1,1,1,1,1], 
    2 : [0,0,0,0], 
    3 : [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
    4 : [0,0,0,0],
    5 : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
    6 : [1,1,1,0,0,1,0,1],
    7 : [0,0,0,0,0,0],
    9 : [0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 
    10 : [0,1,1,1,1,1,0,1,1,,1,1,1,1,0,0,1,0,1,0,1,0,0],
    11 : [1,1,1,0,1,1],
    12 : [0,0,0,0],
    13 : [0,0,0,0,0,0,0,0,0,0,0],
    14 : [0,0,1,0,0,1,0,1,0,0,0,0,0],
    15 : [1,1,1,1,1,1,1,0,1,1],
    16 : [0,0,1,1,1,1,1,1,1,1,1,1,1,1],
    20 : [1,1,1,1,1,1] 
}
onLeftDict = {1: False, 2: False, 3: False, 4: False, 5: True, 6: False, 7: False,
     9:False, 10:False, 11:True, 12 : False, 13:False, 14:False, 15: True, 16:False, 20:False}

def place_paretic_side_first(days_list, patient_id):
    if onLeftDict[patient_id]:
        return days_list
    else:
        for i  in range(len(days_list)):
            for j in range(len(days_list[i])):
                left_measures = days_list[i][j][2:9]
                right_measures = days_list[i][j][11:]
                days_list[i][j] = days_list[i][j][:2] + right_measures + days_list[i][j][9:11] + left_measures
        return days_list

def split_by_day(csv_file, patient_id):
    csv_file.pop(0)
    single_day_list, days_list, current_date = [], [], csv_file[0][0]
    for entry in csv_file:
        if entry[0] == current_date:
            single_day_list.append(entry)
        else:
            current_date = entry[0]
            days_list.append(single_day_list)
            single_day_list = [entry]
    return place_paretic_side_first(days_list, patient_id)

pat1_data = split_by_day(csv_1_list, 1)
pat2_data = split_by_day(csv_2_list, 2)
pat3_data = split_by_day(csv_3_list, 3)
pat4_data = split_by_day(csv_4_list, 4)
pat5_data = split_by_day(csv_5_list, 5)
pat6_data = split_by_day(csv_6_list, 6)
pat7_data = split_by_day(csv_7_list, 7)

pos1reads_affected = []
pos2reads_affected = []
pos3reads_affected = []
pos4reads_affected = []
pos5reads_affected = []
pos6reads_affected = []
pos7reads_affected = []

pos1reads_unaffected = []
pos2reads_unaffected = []
pos3reads_unaffected = []
pos4reads_unaffected = []
pos5reads_unaffected = []
pos6reads_unaffected = []
pos7reads_unaffected = []

patient_list = [pat1_data, pat2_data, pat3_data, pat4_data, pat5_data, pat6_data, pat7_data]


for d in range(len(pat6_data)):
    day = pat6_data[d]
    #print(i + 1, d)
    label = labelsDict[6][d]
    #print("patient ", i + 1 , " label ", label)
    for read in day: 
        try:
            paretic_pos1 = float(read[2])
            paretic_pos2 = float(read[3])
            paretic_pos3 = float(read[4])
            paretic_pos4 = float(read[5])
            paretic_pos5 = float(read[6])
            paretic_pos6 = float(read[7])
            paretic_pos7 = float(read[8])

            non_paretic_pos1 = float(read[11])
            non_paretic_pos2 = float(read[12])
            non_paretic_pos3 = float(read[13])
            non_paretic_pos4 = float(read[14])
            non_paretic_pos5 = float(read[15])
            non_paretic_pos6 = float(read[16])
            non_paretic_pos7 = float(read[17])
            if label == 1:
                pos1reads_affected.append(paretic_pos1 - non_paretic_pos1)
                pos2reads_affected.append(paretic_pos2 - non_paretic_pos2)
                pos3reads_affected.append(paretic_pos3 - non_paretic_pos3)
                pos4reads_affected.append(paretic_pos4 - non_paretic_pos4)
                pos5reads_affected.append(paretic_pos5 - non_paretic_pos5)
                pos6reads_affected.append(paretic_pos6 - non_paretic_pos6)
                pos7reads_affected.append(paretic_pos7 - non_paretic_pos7)
            else:
                pos1reads_unaffected.append(paretic_pos1 - non_paretic_pos1)
                pos2reads_unaffected.append(paretic_pos2 - non_paretic_pos2)
                pos3reads_unaffected.append(paretic_pos3 - non_paretic_pos3)
                pos4reads_unaffected.append(paretic_pos4 - non_paretic_pos4)
                pos5reads_unaffected.append(paretic_pos5 - non_paretic_pos5)
                pos6reads_unaffected.append(paretic_pos6 - non_paretic_pos6)
                pos7reads_unaffected.append(paretic_pos7 - non_paretic_pos7)
        except ValueError:
            pass

num_bins = 20
plt.suptitle("Patient 6 - delirious (blue) vs. non delirious (green)")

plt.subplot(3, 2, 1) 
plt.title("measurment 1")
plt.hist(pos1reads_affected, num_bins, facecolor='blue', alpha=0.5, label='affected')
plt.hist(pos1reads_unaffected, num_bins, facecolor='green', alpha=0.5, label='unaffected')

plt.subplot(3, 2, 2) 
plt.title("measurment 2")
plt.hist(pos2reads_affected, num_bins, facecolor='blue', alpha=0.5, label='affected')
plt.hist(pos2reads_unaffected, num_bins, facecolor='green', alpha=0.5, label='unaffected')

plt.subplot(3, 2, 3) 
plt.title("measurment 3")
plt.hist(pos3reads_affected, num_bins, facecolor='blue', alpha=0.5, label='affected')
plt.hist(pos3reads_unaffected, num_bins, facecolor='green', alpha=0.5, label='unaffected')

plt.subplot(3, 2, 4) 
plt.title("measurment 4")
plt.hist(pos4reads_affected, num_bins, facecolor='blue', alpha=0.5, label='affected')
plt.hist(pos4reads_unaffected, num_bins, facecolor='green', alpha=0.5, label='unaffected')

plt.subplot(3, 2, 5) 
plt.title("measurment 5")
plt.hist(pos5reads_affected, num_bins, facecolor='blue', alpha=0.5, label='affected')
plt.hist(pos5reads_unaffected, num_bins, facecolor='green', alpha=0.5, label='unaffected')

plt.subplot(3, 2, 6) 
plt.title("measurment 6")
plt.hist(pos6reads_affected, num_bins, facecolor='blue', alpha=0.5, label='affected')
plt.hist(pos6reads_unaffected, num_bins, facecolor='green', alpha=0.5, label='unaffected')



plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.55, hspace=0.4)
plt.show()
# print("---------All Patients---------")
# print("Measurement 1")
# print("Affected: sd ", np.std(pos1reads_affected), " mean ", np.mean(pos1reads_affected), " Unaffected: sd ", np.std(pos1reads_unaffected), " mean ", np.mean(pos1reads_unaffected))
# print("Measurement 2")
# print("Affected: sd ", np.std(pos2reads_affected), " mean ", np.mean(pos2reads_affected), " Unaffected: sd ", np.std(pos2reads_unaffected), " mean ", np.mean(pos2reads_unaffected))
# print("Measurement 3")
# print("Affected: sd ", np.std(pos3reads_affected), " mean ", np.mean(pos3reads_affected), " Unaffected: sd ", np.std(pos3reads_unaffected), " mean ", np.mean(pos3reads_unaffected))
# print("Measurement 4")
# print("Affected: sd ", np.std(pos4reads_affected), " mean ", np.mean(pos4reads_affected), " Unaffected: sd ", np.std(pos4reads_unaffected), " mean ", np.mean(pos4reads_unaffected))
# print("Measurement 5")
# print("Affected: sd ", np.std(pos5reads_affected), " mean ", np.mean(pos5reads_affected), " Unaffected: sd ", np.std(pos5reads_unaffected), " mean ", np.mean(pos5reads_unaffected))
# print("Measurement 6")
# print("Affected: sd ", np.std(pos6reads_affected), " mean ", np.mean(pos6reads_affected), " Unaffected: sd ", np.std(pos6reads_unaffected), " mean ", np.mean(pos6reads_unaffected))
# print("Measurement 7")
# print("Affected: sd ", np.std(pos7reads_affected), " mean ", np.mean(pos7reads_affected), " Unaffected: sd ", np.std(pos7reads_unaffected), " mean ", np.mean(pos7reads_unaffected))