import csv 
import tensorflow as tf

# length is 11540 
# line 11528 and on are blank on many of the values 

with open("DW-001-both_merged.csv") as pat_01: csv_1_list = list(csv.reader(pat_01, delimiter=","))


##3
class Model:
    def __init__(self):
        self.logits = self.forward_pass()
        print(self.logits)

    def forward_pass(self):
        return 3

    def g_loss():
        pass
    def d_loss():
        pass
    def optimize():
        pass
    
m = Model() 