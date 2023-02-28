# ref: https://www.w3schools.com/python
import json

# write method to loop through all text files
# append to csv
# add columns for sentiment analysis scores


def get_tweet_data(filepath):
    tweet_list = []
    created_at_list = []
    id_list = []
    file = open(filepath, "r")
    response = file.read()

    js = json.loads(response)
    data = js["data"]
    for tweet in data:
        tweet_text = tweet["text"]
        tweet_created_at = tweet["created_at"]
        tweet_id = tweet["id"]
        tweet_list.append(tweet_text)
        created_at_list.append(tweet_created_at)
        id_list.append(tweet_id)
    print(tweet_list, created_at_list, id_list)


filepath1 = r"C:\Users\kye\Documents\Twitter FYP\post election tweets\post election general\02.12.22 (0400 to 0430).txt"

get_tweet_data(filepath1)
