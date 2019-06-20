import numpy as np 
from stroke_data_parser import StrokeData
from sklearn.linear_model import LinearRegression

actigraph_reads = StrokeData(1, 4)

X_zeros = [] 
X_ones = []
y_zeros = []
y_ones = []
for i in range(len(actigraph_reads.batches)):
    a, b = actigraph_reads.get_next_batch()
    if len(a) > 0:
        if b[0][0] == 0:
            X_zeros.append(a[0])
            y_zeros.append(0)
        else:
            X_ones.append(a[0])
            y_ones.append(0)

X = X_zeros + X_ones
y = y_zeros + y_ones
reg = LinearRegression()
reg.fit(X, y)
print(reg.coef_)