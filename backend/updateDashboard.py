import json
import os
import csv
import re

pos_list, neg_list, neu_list = [], [], []
pos_count, neg_count, neu_count = 0, 0, 0


# write methods to be called in appRoutes.py

# method for piechart
# get total number of respective sentiment tweets (pos, neu, neg)


def get_full_tweet_json(file):
    global pos_list, neu_list, neg_list, pos_count, neu_count, neg_count

    pos_list.clear()
    neu_list.clear()
    neg_list.clear()
    data = []
    if os.path.exists(file):
        with open(file, newline='', encoding='utf8') as inputFile:
            reader = csv.DictReader(inputFile)

            for tweet in reader:
                # geo = tweet['geo']
                # created_at = tweet['created_at']
                # text = tweet['text']
                # neg = tweet['neg']
                # neu = tweet['neu']
                # pos = tweet['pos']
                # compound = tweet['compound']

                overall_sentiment = tweet['overall_sentiment']

                if overall_sentiment == "positive":
                    pos_list.append(tweet)
                elif overall_sentiment == "negative":
                    neg_list.append(tweet)
                elif overall_sentiment == "neutral":
                    neu_list.append(tweet)

                data.append(tweet)

            pos_count = len(pos_list)
            neu_count = len(neu_list)
            neg_count = len(neg_list)

        print(pos_count, neu_count, neg_count)
        return {"data": data}
    else:
        print('File does not exist')


# method to remove brackets and single quotes from string ['1593771032036286465']
# to obtain tweet id: 1593771032036286465

def get_tweet_id(tweet):
    id_string = tweet['edit_history_tweet_ids']
    tweet_id = re.sub("[\[\]']", "", id_string)

    return tweet_id


def pie_chart_data(file):
    get_full_tweet_json(file)
    pc_data = [pos_count, neu_count, neg_count]
    return pc_data


# methods for tweet display
# return tweets by sentiment

def show_tweets(sentiment):
    data = get_full_tweet_json('data/tweets_with_translations.csv')

    tweet_display = {}
    if sentiment == 'positive':
        tweet_display = {"data": pos_list}
    if sentiment == 'negative':
        tweet_display = {"data": neg_list}
    if sentiment == 'neutral':
        tweet_display = {"data": neu_list}
    if sentiment == 'all':
        tweet_display = data
    else:
        print('Please enter "all", "positive", "neutral", or "negative".')

    return tweet_display


