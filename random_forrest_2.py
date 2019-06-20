import numpy as np 
from stroke_data_parser import StrokeData
from single_patient_parser import SinglePatientData
from sklearn.ensemble import RandomForestClassifier


#a = sklearn.ensemble.RandomForestClassifier

actigraph_reads = StrokeData(1, 3)
X =[]
y = []

for i in range(len(actigraph_reads.batches)):
    a, b = actigraph_reads.get_next_batch()
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

test_features = [] 
test_labels = [] 
single_patient_data = SinglePatientData("actigraph_reads/DW-014-both_merged.csv", 14, 1 , 3)
for i in range(len(single_patient_data.batches)):
    a, b = single_patient_data.get_next_batch()
    if len(a) > 0:
        test_features.append(a[0])
        if b[0][0] == 0:
            lbl = 0
        else: 
            lbl = 1
        test_labels.append(lbl)

print(len(test_features))
zero_prediction_zero_label = 0 
one_prediction_one_label = 0
zero_prediction_one_label = 0
one_prediction_zero_label = 0
for i in range(len(test_features)):
    features = test_features[i]
    lbl = test_labels[i]
    pred = clf.predict([features])[0]
    if pred == 0 and lbl == 0:
            zero_prediction_zero_label += 1
    elif pred == 1 and lbl == 1:
        one_prediction_one_label += 1
    elif pred == 0 and lbl == 1:
        zero_prediction_one_label += 1 
    else:
        one_prediction_zero_label += 1

print(zero_prediction_zero_label, one_prediction_one_label, zero_prediction_one_label, one_prediction_zero_label)
total = zero_prediction_zero_label + one_prediction_one_label + zero_prediction_one_label + one_prediction_zero_label
print("zero_prediction_zero_label ", zero_prediction_zero_label, float(zero_prediction_zero_label)/float(total))
print("one_prediction_one_label ", one_prediction_one_label, float(one_prediction_one_label)/float(total))
print("zero_prediction_one_label ", zero_prediction_one_label, float(zero_prediction_one_label)/float(total))
print("one_prediction_zero_label ", one_prediction_zero_label, float(one_prediction_zero_label)/float(total)) 
print("correct ", float(one_prediction_one_label + one_prediction_one_label)/float(total))
