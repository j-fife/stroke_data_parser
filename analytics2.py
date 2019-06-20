import random
from random import sample
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
    7 : [0,0,0,0,0,0]
}
onLeftDict = {1: False, 2: False, 3: False, 4: False, 5: True, 6: False, 7: False}

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

l = [pat1_data, pat2_data, pat3_data, pat4_data, pat5_data, pat6_data, pat7_data]

num_samples = 10

X = []
y = [] 
dataset = [] 
for i in range(len(pat3_data)):
    day = pat3_data[i]
    lbl = labelsDict[3][i] 
    s = sample(day, num_samples)
    for read in s:
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

            t = [paretic_pos6 - non_paretic_pos6, paretic_pos6, non_paretic_pos6]
            X.append(t)
            y.append(lbl)
        except ValueError:
            pass



clf = svm.SVC(kernel='linear', C=1.0)
clf.fit(X,y)
print("finished training")

x_test = []
y_test = []
for i in range(len(pat6_data)):
    day = pat6_data[i]
    lbl = labelsDict[6][i]
    s = sample(day, num_samples)
    for read in s:
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

            t = [paretic_pos6 - non_paretic_pos6, paretic_pos6, non_paretic_pos6]
            x_test.append(t)
            y_test.append(lbl)
        except ValueError:
            pass

for j in range(len(x_test)):
    zero_prediction_zero_label = 0 
    one_prediction_one_label = 0
    zero_prediction_one_label = 0
    one_prediction_zero_label = 0
    pred = clf.predict([x_test[i]])[0]
    print(pred)
    # if pred == 0 and lbl == 0:
    #     zero_prediction_zero_label += 1
    # elif pred == 1 and lbl == 1:
    #     one_prediction_one_label += 1
    # elif pred == 0 and lbl == 1:
    #     zero_prediction_one_label += 1 
    # else:
    #     one_prediction_zero_label += 1 

