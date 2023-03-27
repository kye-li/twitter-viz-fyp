# read csv to dataframe
# run text through sentiment analysis
# add VADER sentiment analysis scores to dataframe
# write dataframe to csv

# vaderSentiment library source code: https://github.com/cjhutto/vaderSentiment
# googleTranslate source code: https://py-googletrans.readthedocs.io/en/latest/
import os
import csv
import re

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import pandas as pd

analyser = SentimentIntensityAnalyzer()     # this line of code taken from reference
translator = Translator()     # this line of code taken from reference

positive_list, negative_list, neutral_list = [], [], []

# tweet_list = []
# translated = []
# trans_origin = []
translations_list = []


# using DictReader: https://docs.python.org/3/library/csv.html#module-contents
def update_tweets_with_sentiment(file):
    global positive_list, negative_list, neutral_list, translations_list

    if os.path.exists(file):
        with open(file, newline='', encoding='utf8') as inputFile:
            with open('data/scored_tweets.csv', 'a', newline='', encoding='utf8') as outputFile:
                reader = csv.DictReader(inputFile)     # this line of code taken from reference
                fieldnames = ['edit_history_tweet_ids', 'geo', 'created_at', 'text', 'neg',      # this line of code taken from reference
                              'neu', 'pos', 'compound', 'overall_sentiment']
                writer = csv.DictWriter(outputFile, fieldnames=fieldnames)     

                if os.stat('data/scored_tweets.csv').st_size == 0:     # this line of code taken from ref: reference: https://thispointer.com/python-three-ways-to-check-if-a-file-is-empty/
                    writer.writeheader()

                for tweet in reader:
                    edit_history_tweet_ids = tweet['edit_history_tweet_ids']
                    geo = tweet['geo']
                    created_at = tweet['created_at']
                    text = tweet['text']
                    # tweet_list.append(text)

                    # translate text to english
                    # major problem as there is a limit to requests to googletrans
                    # The maximum character limit on a single text is 15k.
                    # only 1000 requests per hour
                    # this below is one request.....
                    # more than 11k requests to be done

                    translated_text = translator.translate(text).text     # this line of code taken from reference
                    # print(translated_text)
                    text_scores = analyse_text(translated_text)     
                    neg = text_scores['neg']
                    neu = text_scores['neu']
                    pos = text_scores['pos']
                    compound = text_scores['compound']
                    overall_sentiment = text_scores['overall_sentiment']

                    if overall_sentiment == "positive":
                        positive_list.append(text)
                    elif overall_sentiment == "negative":
                        negative_list.append(text)
                    elif overall_sentiment == "neutral":
                        neutral_list.append(text)

                    new_dict = dict(edit_history_tweet_ids=edit_history_tweet_ids,
                                    geo=geo,
                                    created_at=created_at,
                                    text=text,
                                    neg=neg,
                                    neu=neu,
                                    pos=pos,
                                    compound=compound,
                                    overall_sentiment=overall_sentiment)
                    writer.writerow(new_dict)
                    print(edit_history_tweet_ids)
                    print('row written successfully')
    else:
        print('{file} does not exist')

    print('After translation')
    print('pos:', len(positive_list))
    print('neg:', len(negative_list))
    print('neu:', len(neutral_list))


# read in data
# get text
# run through sentiment analysis
# output on new csv sheet

# to improve on model
# either run through translator or add malay words in lexicon.txt

def analyse_text(tweet):
    sentiment_score_dict = analyser.polarity_scores(tweet)     # this line of code taken from reference
    # method returns a dict with scores in float
    # positive_score = sentiment_score_dict['pos']
    # neutral_score = sentiment_score_dict['neu']
    # negative_score = sentiment_score_dict['neg']
    compound_score = sentiment_score_dict['compound']
    overall_sentiment = ''

    if compound_score >= 0.05:
        overall_sentiment = 'positive'
    elif compound_score <= -0.05:
        overall_sentiment = 'negative'
    elif -0.05 < compound_score < 0.05:
        overall_sentiment = 'neutral'

    sentiment_score_dict["overall_sentiment"] = overall_sentiment

    # print(sentiment_score_dict)
    return sentiment_score_dict


# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.value_counts.html
def get_counts_before_trans(file):
    df1 = pd.read_csv(file)
    total = len(df1["text"])
    print('Tweet counts before translation:')
    print(df1['overall_sentiment'].value_counts(), 'total tweets:', total)     # this line of code taken from reference
    print('')


def get_counts_after_trans(file):
    df2 = pd.read_csv(file)
    total = len(df2["text"])
    print('Tweet counts after translation:')
    print(df2['overall_sentiment'].value_counts(), 'total tweets:', total)    # this line of code taken from reference


# method to remove https links
def remove_links(text):
    new_text = re.sub('(https://\S+)', '', text)
    return new_text


# run tweet through Google Translate
# new dataframe, then read new dataframe to a new csv file

def add_translations_to_data(file):
    links_only = []
    if os.path.exists(file):
        with open(file, newline='', encoding='utf8') as inputFile:
            with open('data/tweets_with_translations.csv', 'a', newline='', encoding='utf8') as outputFile:
                reader = csv.DictReader(inputFile)
                fieldnames = ['edit_history_tweet_ids', 'geo', 'created_at', 'text', 'neg',
                              'neu', 'pos', 'compound', 'overall_sentiment', 'translation']
                writer = csv.DictWriter(outputFile, fieldnames=fieldnames)

                if os.stat('data/tweets_with_translations.csv').st_size == 0:     # this line of code taken from ref: reference: https://thispointer.com/python-three-ways-to-check-if-a-file-is-empty/
                    writer.writeheader()

                for tweet in reader:
                    edit_history_tweet_ids = tweet['edit_history_tweet_ids']
                    geo = tweet['geo']
                    created_at = tweet['created_at']
                    neg = tweet['neg']
                    neu = tweet['neu']
                    pos = tweet['pos']
                    compound = tweet['compound']
                    overall_sentiment = tweet['overall_sentiment']
                    text = tweet['text']

                    translated_text = translator.translate(text).text

                    new_dict = dict(edit_history_tweet_ids=edit_history_tweet_ids,
                                    geo=geo,
                                    created_at=created_at,
                                    text=text,
                                    neg=neg,
                                    neu=neu,
                                    pos=pos,
                                    compound=compound,
                                    overall_sentiment=overall_sentiment,
                                    translation=translated_text
                                    )
                    writer.writerow(new_dict)
                    print(edit_history_tweet_ids)
                    print('row written successfully')
    else:
        print('File does not exist')


# analyse_text(r"I feel very good today, but I am not sad at the same time.")

# update_tweets_with_sentiment('tweets.csv')

# get_counts_before_trans('data/scored_tweets_before_trans.csv')
# get_counts_after_trans('data/scored_tweets.csv')

add_translations_to_data('data/tweets_without_links.csv')
