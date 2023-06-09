import json
import csv
import os
import pandas as pd

# write method to loop through all text files (done)
# append to csv (done)
# remove duplicates (done in Excel)


directory1 = r"C:\Users\kye\Documents\Twitter FYP\election day tweets"
directory2 = r"C:\Users\kye\Documents\Twitter FYP\post election tweets"
directory3 = r"C:\Users\kye\Documents\Twitter FYP\extra pre-election tweets"


# ref: https://docs.python.org/3/library/csv.html
# the open() and DictWriter methods used in code below were re-used code from the Python documentation as referenced

def write_to_csv(data):
    # use 'a' to continue appending rows to original file, 'w' will clear file
    # check first if file is empty, if it is, write header
    with open('data/tweets.csv', 'a', newline='', encoding='utf8') as csvfile:      # taken from reference
        fieldnames = ['edit_history_tweet_ids', 'geo', 'created_at', 'text', 'id']    # taken from reference
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')    # taken from reference

        # check if file is empty, write header
        # reference: https://thispointer.com/python-three-ways-to-check-if-a-file-is-empty/
        if os.stat('data/tweets.csv').st_size == 0:    # this line of code taken from reference
            writer.writeheader()   # this line of code taken from reference (csv.html link above)
            print('file is empty')
        for tweet in data:
            # if Dict has key 'geo', writerow
            # if Dict does not have key 'geo', add new key:value pair, insert an '' empty string
            if 'geo' in tweet:
                writer.writerow(tweet)   # this line of code taken from reference (csv.html link above)
            else:
                tweet['geo'] = ''
                writer.writerow(tweet)   # this line of code taken from reference (csv.html link above)

                
# ref: https://docs.python.org/3/library/os.html
# the os.listdir() method used in code below was written while learning from the Python documentation as referenced

def read_files(directory):
    # take in the directory path
    # if file path ends with .txt
    # open file
    # read file
    # load response as python dict
    # write to csv

    for file in os.listdir(directory):    # this line of code taken from reference
        # https://www.w3schools.com/python/ref_string_format.asp
        filepath = r"{directory}\{file}".format(directory=directory, file=file)    # this line of code taken from reference
        print(filepath)
        f = open(filepath, "r", encoding="utf8")
        response = f.read()
        js = json.loads(response)
        data = js["data"]
        write_to_csv(data)
        print("File read to csv successfully.")
        f.close()


# insert all tweets from txt files into 'tweets.csv' (done)
# read_files(directory1)
# print('election tweets done')
# read_files(directory2)
# print('post election tweets done')
# read_files(directory3)
# print('extra pre-election tweets done')


# method to remove duplicates
# use pandas, put into dataframe, use drop_duplicates method, and then insert it back to csv

def remove_duplicates():
    tweet_dataframe = pd.read_csv('data/tweets.csv')
    # print(tweet_dataframe)
    tweet_dataframe.drop_duplicates(subset='text', keep='first', inplace=True)
    # print(tweet_dataframe)
    tweet_dataframe.to_csv('tweets.csv', index=False)

# remove_duplicates()
# 11865 tweets left
