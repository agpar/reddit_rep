from sklearn.tree import DecisionTreeClassifier
import random
import numpy as np

from experiments.load_vectors import load_file
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.svm import SVC
from sklearn.preprocessing import normalize

def disc(score, y_low):
    if score < 1:
        return 0
    else:
        return 1

def split(header, rows):
    X = []
    Y = []
    wc_ind = header.index('word_count')
    prof_ind = header.index('score')
    for row in rows:
        X.append(row[:wc_ind])
        Y.append(row[prof_ind])
    return X, Y

def use_feats(feat_names, header, rows):
    new_rows = [list() for r in rows]
    for feat in feat_names:
        feat_ind = header.index(feat)
        for nr, r in zip(new_rows, rows):
            nr.append(r[feat_ind])

    return new_rows


def extract_test(X_train, Y_train, size = 500):
    X_pos = [x for x, y in zip(X_train, Y_train) if y == 1]
    X_neg = [x for x, y in zip(X_train, Y_train) if y == 0]

    X_test, Y_test = [], []
    for label in range(0, 2):
        for i in range(0, int(size/2)):
            if label == 0:
                X_test.append(X_neg.pop())
                Y_test.append(label)
            if label == 1:
                X_test.append(X_pos.pop())
                Y_test.append(label)

    X_train, Y_train = [], []
    for x in X_pos:
        X_train.append(x)
        Y_train.append(1)
    for x in X_neg:
        X_train.append(x)
        Y_train.append(0)

    return X_train, Y_train, X_test, Y_test

header, rows, ids = load_file()
X, Y = split(header, rows)

y_sort = [y for y in Y]
y_sort.sort()
y_low = y_sort[int(len(y_sort)/2)]
Y_disc = [disc(y, y_low) for y in Y]

X_trainw, Y_trainw, X_testw, Y_testw = extract_test(X,Y_disc, size=2000)
rfcw = SVC(class_weight='balanced', gamma='scale', C=10).fit(X_trainw, Y_trainw)
#rfcw = DecisionTreeClassifier(max_depth=500, class_weight='balanced').fit(X_trainw, Y_trainw)
#rfcw = RandomForestClassifier(n_estimators=1000, max_depth=6, class_weight='balanced').fit(X_trainw, Y_trainw)
print("With test acc: ", accuracy_score(Y_testw, rfcw.predict(X_testw)))
print("With test prec: ", precision_score(Y_testw, rfcw.predict(X_testw)))
print("With test rec: ", recall_score(Y_testw, rfcw.predict(X_testw)))
