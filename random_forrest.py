import numpy as np 
from stroke_data_parser import StrokeData
from sklearn.ensemble import RandomForestClassifier


#a = sklearn.ensemble.RandomForestClassifier

actigraph_reads = StrokeData(1, 4, True, [1,2,3,4])
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

split = 0.8
l = len(X)

delimiter = int(split*l)

train_features, train_labels = X[:delimiter], y[:delimiter]
test_features, test_labels = X[delimiter:], y[delimiter:]

clf = RandomForestClassifier()
clf.fit(train_features, train_labels)

print("finished training")
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
total = zero_prediction_zero_label + one_prediction_one_label + zero_prediction_one_label + one_prediction_zero_label
print("zero_prediction_zero_label ", zero_prediction_zero_label, float(zero_prediction_zero_label)/float(total))
print("one_prediction_one_label ", one_prediction_one_label, float(one_prediction_one_label)/float(total))
print("zero_prediction_one_label ", zero_prediction_one_label, float(zero_prediction_one_label)/float(total))
print("one_prediction_zero_label ", one_prediction_zero_label, float(one_prediction_zero_label)/float(total)) 
print("correct ", float(one_prediction_one_label + one_prediction_one_label)/float(total))
