import os
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class UniqueFile:
    name: str
    size: int
    date_modified: float


def save_files_as_csv(files, path):
    with open(path, 'w') as f:
        for file, path in files.items():
            f.write(f"{path},{file.name},{file.size},{file.date_modified}\n")


def save_matches_as_csv(matches, path):
    with open(path, 'w') as f:
        pass


def load_files_from_csv(path):
    results = {}
    with open(path, 'r') as f:
        for line in f:
            (root, name, size, date_modified) = line.split(',')
            size = int(size)
            date_modified = float(date_modified)
            unique_file = UniqueFile(name, size, date_modified)
            results[unique_file] = root
    return results


# Recurses through the directory and returns a dictionary of UniqueFile objects mapped to their path
def recurse_files(path):
    results = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            unique_file = UniqueFile(file, os.path.getsize(full_path), round(os.path.getmtime(full_path), 3))
            results[unique_file] = root
    return results


def index_directory(directory, index_file):
    files = recurse_files(directory)
    save_files_as_csv(files, index_file)


# Parses the csv file and matches the files in the directory to the files in the csv file
def match_directory(directory, index_file, matched_file, unmatched_file):
    files = recurse_files(directory)
    indexed_files = load_files_from_csv(index_file)
    matched = []
    unmatched = []
    for unique_file, path in files.items():
        if unique_file in indexed_files:
            match_path = indexed_files.pop(unique_file)
            matched.append((match_path, path, unique_file))
        else:
            unmatched.append((path, unique_file))

    with open(matched_file, 'w') as f:
        f.write("match_root,root,name,size,date_modified\n")
        for match in matched:
            (match_path, path, unique_file) = match
            f.write(f"{match_path},{path},{unique_file.name},{unique_file.size},{unique_file.date_modified}\n")

    with open(unmatched_file, 'w') as f:
        f.write("Old Directory\n")
        f.write("root,name,size,date_modified\n")
        for unique_file, path in indexed_files.items():
            f.write(f"{path},{unique_file.name},{unique_file.size},{unique_file.date_modified}\n")

        f.write("New Directory\n")
        f.write("root,name,size,date_modified\n")
        for match in unmatched:
            (path, unique_file) = match
            f.write(f"{path},{unique_file.name},{unique_file.size},{unique_file.date_modified}\n")


def parse_from_csv():
    path = "files.csv"
    files = load_files_from_csv(path)
    print(files)


index_directory("C:\\Users", "files.csv")
match_directory("C:\\Users", "files.csv", "matched.csv", "unmatched.csv")