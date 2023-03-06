import json
import os
import csv
import re
import nltk
from nltk.tokenize import word_tokenize
# from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
from collections import Counter

nltk.download('punkt')
nltk.download("wordnet")
nltk.download("omw-1.4")

# ps = PorterStemmer()

wnl = WordNetLemmatizer()
factory = StemmerFactory()
stemmer = factory.create_stemmer()

pos_list, neg_list, neu_list = [], [], []
pos_count, neg_count, neu_count = 0, 0, 0

most_occur = []


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

        # print(pos_count, neu_count, neg_count)
        # print(len(data))
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


# ref: https://www.geeksforgeeks.org/find-k-frequent-words-data-set-python/
# ref: https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
# method to return words by its frequency after removing RT@, mentions, and all other special characters
# can be used for word cloud

# concatenate to one long string
# remove RT@, mentions, punctuation, other special chars
# tokenize string with
# from nltk.tokenize import word_tokenize
# word_tokenize(text)
# if not in stopwords, append to list
# pass list into Counter
# run most-common function
def show_word_frequency(file):
    global most_occur
    initial_list, final_list, word_cloud_input = [], [], []
    data = get_full_tweet_json(file)
    data1 = data["data"]
    # get full list of tweets

    for tweet in data1:
        tweet_text = tweet["text"]
        # for each tweet, clean tweet
        lemmatized_words = clean_text(tweet_text)
        # lemmatized_words is a list of words from the tweet
        eng_stopwords = stopwords.words('english')
        ind_stopwords = stopwords.words('indonesian')
        for word in lemmatized_words:
            initial_list.append(word)
            # a list to check how many words initially without excluding stopwords
            if word not in eng_stopwords and word not in ind_stopwords and not word.isnumeric():
                final_list.append(word)
                # a list to check how many words after excluding stopwords and numbers
                # in both eng and indonesian (similar to malay)

    # print(initial_list)
    # print(len(initial_list))
    # print(final_list)
    # print(len(final_list))
    counter = Counter(final_list)
    most_occur = counter.most_common(100)

    for i in most_occur:
        word_and_size = {"text": i[0], "value": i[1]}
        word_cloud_input.append(word_and_size)

    return word_cloud_input


def clean_text(text):
    list_of_words_per_tweet = []
    # remove RT @abcde1234:
    cleaned_text = re.sub("RT @\w+: ", "", text)
    # remove @abcde1234
    cleaned_text1 = re.sub("@\w+ ", "", cleaned_text)
    # remove all special characters (everything except alphabets and digits)
    cleaned_text2 = re.sub("[^a-zA-Z0-9]", " ", cleaned_text1)
    # tokenize string after making them all lowercase
    cleaned_text3 = word_tokenize(str.lower(cleaned_text2))
    # stemming words ref: https://www.geeksforgeeks.org/python-stemming-words-with-nltk/
    # lemmatiztion ref: https://www.datacamp.com/tutorial/stemming-lemmatization-python
    # https://www.nltk.org/_modules/nltk/stem/wordnet.html
    for word in cleaned_text3:
        # english lemmatization
        # "v" as verbs - return lemma of all verbs
        # lemmatized_word = wnl.lemmatize(word, "v")
        # indonesian (similar to malay) stemming and lemmatization
        # https://pypi.org/project/PySastrawi/
        # ref: https://malaya.readthedocs.io/en/latest/load-stemmer.html
        # print(word, " : ", stemmer.stem(word))
        lemmatized_word = stemmer.stem(word)
        list_of_words_per_tweet.append(lemmatized_word)

    # print(list_of_words_per_tweet)
    return list_of_words_per_tweet


# make keyword lower case
# for each tweet
# lower case text
# find match for tweet text
# if yes, append to list
# return {"data": list}
# ref: https://www.w3schools.com/python/python_regex.asp#findall
def show_tweets_by_keyword(keyword):
    tweet_list = []
    keyword = str.lower(keyword)
    data = get_full_tweet_json('data/tweets_with_translations.csv')
    data1 = data["data"]
    for tweet in data1:
        text = str.lower(tweet["text"])
        x = re.findall(keyword, text)
        # if x is not an empty list, meaning there's a match, append tweet to tweet_list
        if x:
            tweet_list.append(tweet)
    if tweet_list:
        response = {"data": tweet_list}
    else:
        response = 'No match, please enter a different keyword.'
    return response


def show_total_tweet_counts(sentiment):
    tweet_count = []
    data = show_tweets(sentiment)
    data1 = data["data"]
    for tweet in data1:
        tweet_count.append(tweet)

    return len(tweet_count)


# method to delete irrelevant tweets
def delete_tweet_from_database(keyword):
    return []

