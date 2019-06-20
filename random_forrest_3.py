import numpy as np 
import sys
from stroke_data_parser import StrokeData
from single_patient_parser import SinglePatientData
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt


#a = sklearn.ensemble.RandomForestClassifier

total_patients = [1,2,3,4,5,6,7,9,10,11,13,14,15,16]
test_patient = int(sys.argv[1])

total_patients.remove(test_patient)
actigraph_reads_train = StrokeData(1, 4, True, total_patients)

patient_reads_test = StrokeData(1, 5, False, [test_patient])

X =[]
y = []

for i in range(len(actigraph_reads_train.batches)):
    a, b = actigraph_reads_train.get_next_batch()
    if len(a) > 0:
        X.append(a[0])
        if b[0][0] == 0:
            lbl = 0
        else: 
            lbl = 1
        y.append(lbl)


clf = RandomForestClassifier()
clf.fit(X, y)
print("finished training")


def parse_hour(time_string):
    x = time_string.split(":")
    try:
        h = int(x[0])
        return h
    except ValueError:
        return -1


hours_total_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
hours_correct_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


#test_features = []
#test_labels = []

zero_prediction_zero_label = 0 
one_prediction_one_label = 0
zero_prediction_one_label = 0
one_prediction_zero_label = 0

for i in range(len(patient_reads_test.batches)):
    a, b = patient_reads_test.get_next_batch()
    if len(a) > 0:
        test_features = a[0][2:] 
        if b[0][0] == 0:
            lbl = 0
        else: 
            lbl = 1
        h = parse_hour(a[0][1])
        if h != -1:
            pred = clf.predict([test_features])
            if pred == 0 and lbl == 0:
                zero_prediction_zero_label += 1
                hours_total_count[h] = hours_total_count[h] + 1
                hours_correct_count[h] = hours_correct_count[h] + 1
            elif pred == 1 and lbl == 1:
                one_prediction_one_label += 1
                hours_total_count[h] = hours_total_count[h] + 1
                hours_correct_count[h] = hours_correct_count[h] + 1
            elif pred == 0 and lbl == 1:
                hours_total_count[h] = hours_total_count[h] + 1
                zero_prediction_one_label += 1 
            else:
                hours_total_count[h] = hours_total_count[h] + 1
                one_prediction_zero_label += 1

hrs = []
hr_acc = []
for i in range(len(hours_correct_count)):
    hrs.append(i)
    hr_acc.append(float(hours_correct_count[i])/float(hours_total_count[i]))


s = ""
r = ""
for i in range(len(hrs)):
    s = s + ", " + str(round(hr_acc[i], 2))
    r = r + ",  " + str(hours_total_count[i])

print(s[2:])
print(r[2:])




fig = plt.figure()
fig.suptitle('Patient ' + str(test_patient), fontsize=14, fontweight='bold')
plt.xticks(hrs)
plt.xlabel('Hour', fontsize=10)
plt.ylabel('Accuracy', fontsize=10)
plt.ylim((0.0, 1.0))
plt.plot(hrs, hr_acc)
plt.show()


#print(test_features[:10])
#print(test_labels[:10])
