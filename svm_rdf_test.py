import time
import matplotlib.pyplot as ptl
import numpy as np

from sklearn.datasets import fetch_mldata
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.utils import check_random_state

# 70000*784
mnist = fetch_mldata("MNIST original")
X, y = mnist.data /255, mnist.target
# X = X[:7000]
# y= y[:7000]

time_begin = time.localtime()
print("start time {}:{}:{}".format(time_begin.tm_hour, time_begin.tm_min, time_begin.tm_sec))
print("raw data size:{}, {}".format(X.shape, y.shape))
random_state = check_random_state(0)
permutation = random_state.permutation(X.shape[0])
X = X[permutation]
y = y[permutation]
X = X.reshape((X.shape[0], -1))
n_test =10000
X_train, X_test, y_train, y_test = train_test_split(
    X, y, train_size=60000, test_size=n_test)
print("x_train:{}, y_train:{},  X_test:{}, y_test:{}".format(X_train.shape, X_test.shape, y_train.shape, y_test.shape))

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

clf = SVC()
clf.fit(X_train, y_train)
y_predict = clf.predict(X_test)

positive = 0
for pair in zip(y_predict, y_test):
    if pair[0] == pair[1]:
        positive += 1

print("rate:{}".format(positive/n_test))
time_end = time.localtime()
print("end time {}:{}:{}".format(time_end.tm_hour, time_end.tm_min, time_end.tm_sec))