import tensorflow as tf
import numpy as np
from stroke_data_parser import StrokeData

num_classes = 2 
batch_size = 5
num_values = 21

n_nodes_l1 = 100
hl2_size = 5

actigraph_reads = StrokeData(batch_size)
#a, b = actigraph_reads.get_next_batch()

#b, l = data_manager.get_next_batch()
#print(b) 
#print(l)

## try to implement one hot like this guy 
# https://www.youtube.com/watch?v=PwAGxqrXSCs&list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRn5v&index=47
#
class Model:
    def __init__(self, read, label):
        self.read = read
        self.label = label
        self.prediction = self.forward_pass()
        self.loss = self.loss_function()
        self.optimize = self.optimizer()
        self.accuracy = self.accuracy_function()
    
    def forward_pass(self):
        size1 = 300
        size2 = 50
        size3  =25
        layer1 = tf.Variable(tf.random_normal([num_values, size1]))
        bias1 = tf.Variable(tf.random_normal([size1]))

        layer2 =  tf.Variable(tf.random_normal([size1, size2]))
        bias2 = tf.Variable(tf.random_normal([size2]))

        layer3 =  tf.Variable(tf.random_normal([size2, size3]))
        bias3 = tf.Variable(tf.random_normal([size3]))

        output_layer = tf.Variable(tf.random_normal([size3, num_classes]))
        bias_out = tf.Variable(tf.random_normal([num_classes]))

        l1 = tf.nn.relu(tf.add(tf.matmul(self.read, layer1), bias1))
        l2 = tf.nn.relu(tf.add(tf.matmul(l1, layer2), bias2))
        l3 = tf.nn.relu(tf.add(tf.matmul(l2, layer3), bias3))
        output = tf.add(tf.matmul(l3, output_layer), bias_out)
        return output
    
    def loss_function(self):
        return tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.label, logits=self.prediction))
        #return tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.label, logits=self.prediction)
    
    def optimizer(self):
        return tf.train.AdamOptimizer(0.00001).minimize(self.loss)
    
    def accuracy_function(self):
        return -1

x = tf.placeholder(dtype='float', shape=[None, num_values])
y = tf.placeholder(dtype='float', shape=[None, num_classes])

m = Model(x, y)

a, b = actigraph_reads.get_next_batch()

session = tf.Session()
session.run(tf.global_variables_initializer())


for i in range(len(actigraph_reads.batches )-200):
    a, b = actigraph_reads.get_next_batch()
    l, _ = session.run([m.loss, m.optimize], feed_dict={x: a, y: b})
    if (i % 20) == 0:
        print("iteration ", i , " loss ", l)