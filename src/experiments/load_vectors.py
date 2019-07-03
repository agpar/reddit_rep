import numpy as np
import csv
VECTOR_FILE = "./data/vectors2.csv"

def load_file(vector_file=VECTOR_FILE):
    rows = []
    ids = []
    with open(vector_file, 'r') as f:
        reader = csv.reader(f)
        header = reader.__next__()[1:]
        for line in reader:
            ids.append(line[0])
            rows.append(np.array([float(x) for x in line[1:]]))
    return header, rows, ids