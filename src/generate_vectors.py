from trees import GenerateTrees
import csv
import os

OUTPUT_FILE = "data/vectors.csv"
counter = 0
max_trees = 90_000
force_fresh = False

if force_fresh and os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

file_exists = os.path.exists(OUTPUT_FILE)


# Take stock of what we've already porocessed
seen_roots = set()
if file_exists:
    with open(OUTPUT_FILE, 'r') as f:
        for line in f:
            seen_roots.add(line.split(",")[0])

counter = 0
with open(OUTPUT_FILE, 'a') as f:
    csvwriter = csv.writer(f)

    if max_trees:
        print(f"Generating up to {max_trees} trees.")

    for tree in GenerateTrees(seen_roots):
        if (not file_exists):
            csvwriter.writerow(["root_id"] + tree.vector_labels())
            file_exists = True
        if tree.is_valid():
            csvwriter.writerow([tree.comment_id] + tree.to_vector())
            counter += 1
            if counter == max_trees:
                break

        if counter > 0 and counter % 1000 == 0:
            print(f"Generated {counter} trees.")

