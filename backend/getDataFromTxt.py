# ref: https://www.w3schools.com/python
# ref: https://docs.python.org/3/library/os.html

import json
import csv
import os

# write method to loop through all text files (done)
# append to csv (done)
# remove duplicates (done in Excel)


directory1 = r"C:\Users\kye\Documents\Twitter FYP\election day tweets"
directory2 = r"C:\Users\kye\Documents\Twitter FYP\post election tweets"


def write_to_csv(data):
    # use 'a' to continue appending rows to original file, 'w' will clear file
    # check first if file is empty, if it is, write header
    with open('tweets.csv', 'a', newline='', encoding='utf8') as csvfile:
        fieldnames = ['edit_history_tweet_ids', 'geo', 'created_at', 'text', 'id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')

        # check if file is empty, write header
        # reference: https://thispointer.com/python-three-ways-to-check-if-a-file-is-empty/
        if os.stat('tweets.csv').st_size == 0:
            writer.writeheader()
            print('file is empty')
        for tweet in data:
            # if Dict has key 'geo', writerow
            # if Dict does not have key 'geo', add new key:value pair, insert an '' empty string
            if 'geo' in tweet:
                writer.writerow(tweet)
            else:
                tweet['geo'] = ''
                writer.writerow(tweet)


def read_files(directory):
    # take in the directory path
    # if file path ends with .txt
    # open file
    # read file
    # load response as python dict
    # write to csv

    for file in os.listdir(directory):
        if file.endswith('.txt'):
            # https://www.w3schools.com/python/ref_string_format.asp
            filepath = r"{directory}\{file}".format(directory=directory, file=file)
            print(filepath)
            f = open(filepath, "r", encoding="utf8")
            response = f.read()
            js = json.loads(response)
            data = js["data"]
            write_to_csv(data)
            print("File read to csv successfully.")
            f.close()
        else:
            print(OSError)

# insert all tweets from txt files into 'tweets.csv' (done)
# read_files(directory1)
# print('election tweets done')
# read_files(directory2)
# print('post election tweets done')

# method to remove duplicates
# (removed it manually on Excel) (48664 tweets were duplicates and were removed, only 11711 left)
