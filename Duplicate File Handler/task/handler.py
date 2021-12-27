import argparse
import os
import hashlib


def show_files(dir, ext, sort):
    files_dict = {}
    for root, dirs, files in os.walk(".", topdown=True):
        for name in files:
            if os.path.getsize(os.path.join(root, name)) > 0:
                if ext != "":
                    if os.path.splitext(name)[-1] == f".{ext}":
                        files_dict[os.path.join(root, name)] = os.path.getsize(os.path.join(root, name))
                else:
                    files_dict[os.path.join(root, name)] = os.path.getsize(os.path.join(root, name))
    duplicates = {}
    for key, value in files_dict.items():
        if value not in duplicates.keys():
            duplicates[value] = [key]
        else:
            duplicates[value].append(key)
    sorted_duplicates = {}
    if sort == "1":
        for i in sorted(duplicates.keys(), reverse=True):
            sorted_duplicates[i] = duplicates[i]
        for value, key in sorted_duplicates.items():
            if len(key) > 1:
                print(value, "bytes")
                for file in key:
                    print(file)
    else:
        for i in sorted(duplicates.keys()):
            sorted_duplicates[i] = duplicates[i]
        for value, key in sorted_duplicates.items():
            if len(key) > 1:
                print(value, "bytes")
                for file in key:
                    print(file)
    return sorted_duplicates


def duplicates(dupl):
    hash_duplicates = {}
    counter = 1
    for value, files in dupl.items():
        if len(files) > 1:
            tmp_hash_duplicates = {}
            for file in files:
                open_file = open(file, 'rb')
                hash_of_file = hashlib.md5(open_file.read()).hexdigest()
                if hash_of_file not in hash_duplicates.keys():
                    hash_duplicates[hash_of_file] = [file]
                else:
                    hash_duplicates[hash_of_file].append(file)
                if hash_of_file not in tmp_hash_duplicates.keys():
                    tmp_hash_duplicates[hash_of_file] = [file]
                else:
                    tmp_hash_duplicates[hash_of_file].append(file)
                open_file.close()
            print(value, "bytes")
            for value2, files2 in tmp_hash_duplicates.items():
                if len(files2) > 1:
                    print("Hash:", value2)
                    for i in files2:
                        print("{}. {}".format(counter, i))
                        counter += 1


def main():
    parser = argparse.ArgumentParser(description='Input the path.')
    parser.add_argument('path', nargs='?', default="-1")
    path = parser.parse_args()
    if path.path == "-1":
        print("Directory is not specified")
        exit()
    print("Enter file format:")
    format = input()
    print("")
    print("Size sorting options:")
    print("1. Descending")
    print("2. Ascending")
    print("")
    while True:
        print("Enter a sorting option:")
        sorting = input()
        if sorting == "1" or sorting == "2":
            sorted_duplicates = show_files(path.path, format, sorting)
            break
        else:
            print("Wrong option")
    print("Check for duplicates?")
    check_duplicates = input()
    if check_duplicates == "yes":
        duplicates(sorted_duplicates)


main()
