"""Definitions, imports."""
import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.svm import SVC
from sklearn.preprocessing import normalize

VECTOR_FILE = 'data/vectors_new.csv'

def load_file(vector_file=VECTOR_FILE):
    rows = []
    ids = []
    with open(VECTOR_FILE, 'r') as f:
        reader = csv.reader(f)
        header = reader.__next__()[1:]
        for i, line in enumerate(reader):
            ids.append(line[0])
            rows.append(np.array([float(x) for x in line[1:]]))
    return header, np.array(rows), ids


def disc_scores(score):
    if score < 1:
        return 0
    elif score == 1.0:
        return None
    else:
        return 1


def disc_hateconf(conf):
  if conf < 0.1:
    return 0
  else:
    return 1

def disc_sent(sent):
  if sent < 0:
    return 0
  else:
    return 1

def split(header, rows, target):
    X = []
    Y = []
    wc_ind = header.index('word_count')
    target_ind = header.index(target)
    for row in rows:
        X.append(row[:wc_ind])
        Y.append(row[target_ind])
    return np.array(X), np.array(Y)


def use_feats(feat_names, header, rows):
    new_rows = [list() for r in rows]
    for feat in feat_names:
        feat_ind = header.index(feat)
        for nr, r in zip(new_rows, rows):
            nr.append(r[feat_ind])

    return new_rows


def extract_test(X_train, Y_train, size = 1000):
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

### FILE LOADING
header, rows, ids = load_file()
print(len(rows))


"""Test setup"""
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.model_selection import StratifiedShuffleSplit

# The number of discretizations to apply to the score
n_bins = 2

# Transform rows and headers into X and Y, based on the value we want to predict
X, Y = split(header, rows, 'sent')

# Sklearn bin discreatization
# est = KBinsDiscretizer(n_bins=n_bins, encode='ordinal', strategy='uniform')
# est.fit(Y.reshape(-1, 1))
# Y_disc = est.transform(Y.reshape(-1, 1))
# print(est.bin_edges_)

# Homegrown discretization
Y_disc = np.array([disc_sent(y) for y in Y if disc_sent(y) is not None])

# Sklearn data splitting
# sss = StratifiedShuffleSplit(n_splits=1, test_size=0.1, random_state=0)
# train_index, test_index = sss.split(X, Y_disc).__next__()
# X_train, X_test = X[train_index], X[test_index]
# Y_train, Y_test = Y_disc[train_index], Y_disc[test_index]

# Homegrown data splitting
X_train, Y_train, X_test, Y_test = extract_test(X, Y_disc, 5000)

print("Pos tests ", sum(1 for y in Y_test if y==1)/len(Y_test))
print("Neg tests ", sum(1 for y in Y_test if y==0)/len(Y_test))
print("Pos examples ", sum(1 for y in Y_train if y==1), " ", sum(1 for y in Y_train if y==1)/len(Y_train))
print("Neg examples ", sum(1 for y in Y_train if y==0), " ", sum(1 for y in Y_train if y==0)/len(Y_train))
feats = list(zip(header, X_train[0]))
print(header)
assert('score' not in [f[0] for f in feats])


"""Random Forest EXPERIMENT"""
from sklearn.ensemble import RandomForestClassifier
import time

start = time.time()
rfcw = RandomForestClassifier(n_estimators=200, max_depth=8, class_weight='balanced').fit(X_train, Y_train)
end = time.time()

predictions = rfcw.predict(X_test)
print("Acc: ", accuracy_score(Y_test, predictions))
print("Prec: ", precision_score(Y_test, predictions))
print("Rec: ", recall_score(Y_test, predictions))
print(f"Trained in {end-start}")

feats = list(zip(header, rfcw.feature_importances_))
feats.sort(key=lambda x: -x[1])
print(feats[:20])