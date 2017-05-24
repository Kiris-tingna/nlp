#coding=utf-8
import tensorflow as tf
import numpy as np
#mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
x = tf.placeholder(tf.float32, [None, 1])
W = tf.Variable(tf.zeros([1,3]))
b = tf.Variable(tf.zeros([3]))
y = tf.nn.softmax(tf.matmul(x,W) + b)
y_ = tf.placeholder("float", [None,3])
cross_entropy = -tf.reduce_sum(y_*tf.log(y+1e-10))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)
#对0-100，100-200，200-300 进行分类
x_data_1=np.linspace(0,100,100);
x_data_2=np.linspace(100,200,100)
x_data_3=np.linspace(200,300,100)

x_data=np.concatenate((x_data_1,x_data_2,x_data_3)).reshape(-1,1)

y_data=np.array([1,0,0]*100+[0,1,0]*100+[0,0,1]*100).reshape(-1,3)


for i in range(200):

  sess.run(train_step, feed_dict={x: x_data, y_: y_data})
  correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_data, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
  if i%50==0:
    #print sess.run(accuracy, feed_dict={x: x_data, y_: y_data})
    www = sess.run(W)
    bbb = sess.run(b)
    ccc= sess.run(cross_entropy, feed_dict={x: x_data, y_: y_data})
    yyy=sess.run(y,feed_dict={x: x_data})
    print(ccc)




print sess.run(tf.argmax(y, 1),feed_dict={x:[[0.7],[1.3],[288],[1.7],[2222.2],[3.333]]})