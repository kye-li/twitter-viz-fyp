import numpy as np
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re as re
import pandas as pd
from PIL import Image
from wordcloud import WordCloud, STOPWORDS

client = tweepy.Client(
    "AAAAAAAAAAAAAAAAAAAAAEdchgEAAAAAoMYohigl0ivRkDXA0Xbxm%2FC7BhM%3D2RV4sBsPfRtOfRRASXHrv50t0It6RGRDnXmHCusBNUgACJMu8q")

# search Twitter for a term
# ref: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent

negative_score = 0.0
positive_score = 0.0
neutral_score = 0.0
compound_score = 0.0

totalPositive = 0
totalNegative = 0
totalNeutral = 0

totalTweets = 0
positivePer = 0.0
negativePer = 0.0
neutralPer = 0.0

tweet_list = []
cleaned_list = []
positive_list = []
negative_list = []
neutral_list = []

# ref: https://www.geeksforgeeks.org/python-sentiment-analysis-using-vader/
# do sentiment analysis using vader
def sentiment_scores(sentence):
    global negative_score, positive_score, neutral_score, compound_score
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # add new words to the lexicon
    # new_words = {
    # 'boleh': 2.0,
    # 'gembira': 5.0,
    # }

    # sid_obj.lexicon.update(new_words)
    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)

    negative_score = sentiment_dict['neg']
    neutral_score = sentiment_dict['neu']
    positive_score = sentiment_dict['pos']
    compound_score = sentiment_dict['compound']


def get_and_score_tweets(keyword):
    global totalPositive, totalNeutral, totalNegative
    global totalTweets, positivePer, neutralPer, negativePer
    global tweet_list, cleaned_list, positive_list, neutral_list, negative_list

    positive = 0
    negative = 0
    neutral = 0

    data = []
    tweet_list.clear()
    cleaned_list.clear()
    positive_list.clear()
    neutral_list.clear()
    negative_list.clear()

    new_tweets = tweepy.Paginator(client.search_recent_tweets, keyword,
                                  max_results=100).flatten(10)

    # append cleaned tweet to cleaned_tweets array and loop through it below
    for tweet in new_tweets:
        tweet_list.append(tweet.text)

        # append tweet.text to new array
        # run array through clean_tweets function
        # clean_tweets function returns an array of cleaned tweets
        # run sentiment analysis for every cleaned_tweet

    cleaned_list = clean_tweets(tweet_list)

    for cleaned_tweet in cleaned_list:
        scored_tweets = {"text": None, "sentiment": None}
        #    print(tweet.id, tweet.text)
        # translate sentence to eng
        # if tweet.text != "\n":
        #    tweet.text = translator.translate(tweet.text).text

        sentiment_scores(cleaned_tweet)

        # decide sentiment as positive, negative and neutral
        if compound_score >= 0.05:
            sentiment = "Positive"
            positive += 1
            positive_list.append(cleaned_tweet)
            # print("Positive")

        elif compound_score <= - 0.05:
            sentiment = "Negative"
            negative += 1
            negative_list.append(cleaned_tweet)
            # print("Negative")

        else:
            sentiment = "Neutral"
            neutral += 1
            neutral_list.append(cleaned_tweet)
            # print("Neutral")

        scored_tweets["text"] = cleaned_tweet
        scored_tweets["sentiment"] = sentiment
        data.append(scored_tweets)

    totalPositive = positive
    totalNegative = negative
    totalNeutral = neutral

    # print(tweet_list)
    return {"data": data}
    # totalTweets = positive + negative + neutral
    # positivePer = round(100 * (positive / totalTweets), 2)
    # negativePer = round(100 * (negative / totalTweets), 2)
    # neutralPer = round(100 * (neutral / totalTweets), 2)

    # print(totalTweets, positivePer, negativePer, neutralPer)


def get_pie_data(keyword):
    get_and_score_tweets(keyword)
    return [totalNegative, totalNeutral, totalPositive]


# function to drop duplicated and remove RT, returns a list
def clean_tweets(tw_list):
    # drop duplicates
    tw_list = pd.DataFrame(tw_list)
    tw_list.drop_duplicates(inplace=True)
    tw_list["text"] = tw_list[0]
    tw_list["text"] = tw_list.text.map(remove_rt())
    tw_list = tw_list["text"].values.tolist()
    return tw_list


# function to remove 'RT@'
def remove_rt():
    return lambda x: re.sub('RT @\w+: ', " ", x)


# function to remove url links, mentions and all special char (everything except digits and alphabets)
def remove_mentions():
    return lambda x: re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", x)
# comment source

def word_cloud_input(tw_list):
    tw_list = pd.DataFrame(tw_list)
    tw_list["text"] = tw_list[0]
    tw_list["text"] = tw_list.text.map(remove_mentions())
    tw_list["text"] = tw_list.text.str.lower()
    return tw_list["text"]

# source: https://towardsdatascience.com/step-by-step-twitter-sentiment-analysis-in-python-d6f650ade58d
def create_wordcloud(text):
    mask = np.array(Image.open("../wcBG.png"))
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color="white",
                   mask=mask,
                   max_words=3000,
                   stopwords=stopwords,
                   repeat=True)
    wc.generate(str(text))
    wc.to_file("../wc.png")
    print("Word Cloud Saved Successfully")
    # path = "../wc.png"
    # image = Image.open(path)
    # image.show()


def get_wordcloud(keyword):
    get_and_score_tweets(keyword)
    x = word_cloud_input(cleaned_list)
    create_wordcloud(x.values)


# get_and_score_tweets('scotland')
# y = word_cloud_input(positive_list)
# z = word_cloud_input(neutral_list)
# a = word_cloud_input(negative_list)

# Creating wordcloud for all tweets
# create_wordcloud(y.values)
# create_wordcloud(z.values)
# create_wordcloud(a.values)


# Creating wordcloud for positive sentiment
# create_wordcloud(tw_list_positive["text"].values)

# Creating wordcloud for negative sentiment
# create_wordcloud(tw_list_negative["text"].values)

# Creating wordcloud for neutral sentiment
# create_wordcloud(tw_list_neutral["text"].values)
#
#
# def word_cloud(keyword):
#     # function to generate word cloud
#     return ''
#
#
# def line_chart(keyword):
#     # function to create line chart to look at when tweets are tweeted out
#     return ''
