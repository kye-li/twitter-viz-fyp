# read csv to dataframe
# run text through sentiment analysis
# add VADER sentiment analysis scores to dataframe
# write dataframe to csv

# vaderSentiment library source code: https://github.com/cjhutto/vaderSentiment
# googleTranslate source code: https://py-googletrans.readthedocs.io/en/latest/
import os
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator

analyser = SentimentIntensityAnalyzer()
translator = Translator()

positive_list = []
negative_list = []
neutral_list = []

# tweet_list = []
# translated = []
# trans_origin = []
translations_list = []


# using DictReader: https://docs.python.org/3/library/csv.html#module-contents
def update_tweets_with_sentiment(file):
    global positive_list, negative_list, neutral_list, translations_list

    if os.path.exists(file):
        with open(file, newline='', encoding='utf8') as inputFile:
            with open('scored_tweets.csv', 'a', newline='', encoding='utf8') as outputFile:
                reader = csv.DictReader(inputFile)
                fieldnames = ['edit_history_tweet_ids', 'geo', 'created_at', 'text', 'neg',
                              'neu', 'pos', 'compound', 'overall_sentiment']
                writer = csv.DictWriter(outputFile, fieldnames=fieldnames)

                if os.stat('scored_tweets.csv').st_size == 0:
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

                    translated_text = translator.translate(text).text
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
    sentiment_score_dict = analyser.polarity_scores(tweet)
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


# def google_translate(t_list):
#     global translated, trans_origin
#     translations = translator.translate(t_list)
#     for translation in translations:
#         translated.append(translation.text)
#         trans_origin.append(translation.origin)
#
#     print(len(translated), len(trans_origin))
# analyse_text(r"I feel very good today, but I am not sad at the same time.")

update_tweets_with_sentiment('tweets.csv')


