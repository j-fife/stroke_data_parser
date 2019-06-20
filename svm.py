import numpy as np 
from stroke_data_parser import StrokeData
from sklearn import svm

actigraph_reads = StrokeData(1, 3)
a, b = actigraph_reads.get_next_batch()

X =[]
y = []

test_number = 1000
train_number = 20000
total_reads = len(actigraph_reads.batches)


for i in range(train_number):
    a, b = actigraph_reads.get_next_batch()
    if len(a) > 0:
        X.append(a[0])
        if b[0][0] == 0:
            lbl = 0
        else: 
            lbl = 1
        y.append(lbl)
        
clf = svm.SVC(kernel='linear', C=1.0)
clf.fit(X,y)
print("finished training")

zero_prediction_zero_label = 0 
one_prediction_one_label = 0
zero_prediction_one_label = 0
one_prediction_zero_label = 0
for i in range(test_number):
    a, b = actigraph_reads.get_next_batch()
    if len(a) > 0:
        d = a[0]
        if b[0][0] == 0:
                lbl = 0
        else: 
            lbl = 1
        pred = clf.predict([d])[0]
        if pred == 0 and lbl == 0:
            zero_prediction_zero_label += 1
        elif pred == 1 and lbl == 1:
            one_prediction_one_label += 1
        elif pred == 0 and lbl == 1:
            zero_prediction_one_label += 1 
        else:
            one_prediction_zero_label += 1 

print("zero_prediction_zero_label ", zero_prediction_zero_label)
print("one_prediction_one_label ", one_prediction_one_label)
print("zero_prediction_one_label ", zero_prediction_one_label)
print("one_prediction_zero_label ", one_prediction_zero_label)