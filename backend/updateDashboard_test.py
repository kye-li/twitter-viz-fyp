import unittest
import updateDashboard as uD
import datetime
import re
from collections import Counter


class MyTestCase(unittest.TestCase):
    def test_show_all_tweets(self):
        # file exists
        # check each sentiment list contains correct sentiment tweets
        # returns {"data" : data}
        # file does not exist
        # returns "File does not exist, please ensure file name/location is correct."

        # with default (existing file)
        self.assertTrue(isinstance(uD.show_all_tweets(), dict))
        # with non-existent file
        self.assertTrue(isinstance(uD.show_all_tweets(file=''), str))

        uD.show_all_tweets()

        # if there is data, there should be pos, neu, and neg tweets
        if isinstance(uD.show_all_tweets(), dict):
            self.assertNotEqual(uD.a_pos_list, [])
            self.assertNotEqual(uD.a_neu_list, [])
            self.assertNotEqual(uD.a_neg_list, [])

        # check correct categorisation of tweets into respective lists
        for tweet in uD.a_pos_list:
            self.assertEqual(tweet["overall_sentiment"], "positive")
        for tweet in uD.a_neu_list:
            self.assertEqual(tweet["overall_sentiment"], "neutral")
        for tweet in uD.a_neg_list:
            self.assertEqual(tweet["overall_sentiment"], "negative")

    def test_show_tweets_by_keyword(self):
        # existing keyword
        self.assertTrue(isinstance(uD.show_tweets_by_keyword('GE15'), dict))
        # non-existent keyword
        self.assertTrue(isinstance(uD.show_tweets_by_keyword('scotland'), str))

        data = uD.show_tweets_by_keyword('GE15')
        data1 = data["data"]

        # check if all tweets contains the keyword
        # keyword is converted to lowercase in original method
        tweet_list = []
        for tweet in data1:
            text = str.lower(tweet["text"])
            x = re.findall('ge15', text)
            if x:
                tweet_list.append(tweet)

        self.assertEqual(len(tweet_list), len(data1))

        uD.show_tweets_by_keyword('GE15')

        # check correct categorisation of tweets into respective lists
        for tweet in uD.k_pos_list:
            self.assertEqual(tweet["overall_sentiment"], "positive")
        for tweet in uD.k_neu_list:
            self.assertEqual(tweet["overall_sentiment"], "neutral")
        for tweet in uD.k_neg_list:
            self.assertEqual(tweet["overall_sentiment"], "negative")

    def test_show_tweets_by_sentiment(self):

        # case 1 to case 7 was tested with the default sentiment of 'all'
        # sentiment testing will continue from case 8 onwards

        # case 1: keyword empty, date not empty, tweets available on date
        # check tweets returned has correct date

        c1response = uD.show_tweets_by_sentiment('', 'all', '2022-11-19')
        tweets = c1response["data"]
        for tweet in tweets:
            tweet_datetime = tweet["created_at"]
            tweet_datetime1 = datetime.datetime.fromisoformat(tweet_datetime)
            tweet_date = str(tweet_datetime1.date())
            self.assertEqual(tweet_date, '2022-11-19')

        # case 2: keyword empty, date not empty, tweets not available on date
        # check if error message {error message} returned

        c2response = uD.show_tweets_by_sentiment('', 'all', '2022-12-19')
        self.assertEqual(c2response, {"No tweets available in the database on this date."})

        # case 3: keyword empty, date empty
        # check if correct data retrieved when no keyword input and no date input
        # which is equivalent to show_all_tweets()

        c3response = uD.show_tweets_by_sentiment('', 'all', '')
        self.assertEqual(c3response, uD.show_all_tweets())

        # case 4: keyword not empty, date not empty, tweets available on date for that keyword
        # check if tweets returned contains correct keyword AND date

        c4response = uD.show_tweets_by_sentiment('GE15', 'all', '2022-11-19')
        data1 = c4response["data"]

        # check if all tweets contains the keyword AND correct date
        # keyword is converted to lowercase in original method
        tweet_list = []
        for tweet in data1:
            text = str.lower(tweet["text"])
            x = re.findall('ge15', text)
            if x:
                tweet_list.append(tweet)
            tweet_datetime = tweet["created_at"]
            tweet_datetime1 = datetime.datetime.fromisoformat(tweet_datetime)
            tweet_date = str(tweet_datetime1.date())
            self.assertEqual(tweet_date, '2022-11-19')

        self.assertEqual(len(tweet_list), len(data1))

        # case 5: keyword not empty, date not empty, tweets not available on date for that keyword
        # check if error message string is returned

        c5response = uD.show_tweets_by_sentiment('GE15', 'all', '2022-12-15')
        self.assertEqual(c5response, {"No tweets available in the database on this date."})

        # case 6: keyword not empty, date empty
        # check if correct data retrieved when there is keyword input but no date input
        # which is equivalent to show_tweets_by_keyword(keyword)

        c6response = uD.show_tweets_by_sentiment('GE15', 'all', '')
        self.assertEqual(c6response, uD.show_tweets_by_keyword('GE15'))

        # case 7: no tweets matching the keyword
        # check if error string returned

        c7response = uD.show_tweets_by_sentiment('scotland', 'all', '')
        self.assertEqual(c7response, {"No match, please enter a different keyword."})

        # case 8: positive, positive tweets returned
        c8response = uD.show_tweets_by_sentiment('GE15', 'positive', '')
        tweets = c8response["data"]
        for tweet in tweets:
            sentiment = tweet["overall_sentiment"]
            self.assertEqual(sentiment, "positive")

        # case 9: no positive tweets
        c9response = uD.show_tweets_by_sentiment('goodbye', 'positive', '')
        self.assertEqual(c9response, {"No positive tweets found."})

        # case 10: negative, negative tweets returned
        c10response = uD.show_tweets_by_sentiment('GE15', 'negative', '')
        tweets = c10response["data"]
        for tweet in tweets:
            sentiment = tweet["overall_sentiment"]
            self.assertEqual(sentiment, "negative")

        # case 11: no negative tweets
        c11response = uD.show_tweets_by_sentiment('goodbye', 'negative', '')
        self.assertEqual(c11response, {"No negative tweets found."})

        # case 12: neutral, neutral tweets returned
        c12response = uD.show_tweets_by_sentiment('GE15', 'neutral', '')
        tweets = c12response["data"]
        for tweet in tweets:
            sentiment = tweet["overall_sentiment"]
            self.assertEqual(sentiment, "neutral")

        # case 13: no neutral tweets
        c13response = uD.show_tweets_by_sentiment('hello', 'neutral', '2022-11-19')
        self.assertEqual(c13response, {"No neutral tweets found."})

        # case 14: all sentiments (check if number of tweets for separate calls
        # for 3 different sentiments total up to calling by 'all' sentiments)

        c141response = uD.show_tweets_by_sentiment('ge15', 'positive', '2022-11-19')
        pos_tweet_count = len(c141response["data"])
        c142response = uD.show_tweets_by_sentiment('ge15', 'negative', '2022-11-19')
        neg_tweet_count = len(c142response["data"])
        c143response = uD.show_tweets_by_sentiment('ge15', 'neutral', '2022-11-19')
        neu_tweet_count = len(c143response["data"])
        c14response = uD.show_tweets_by_sentiment('ge15', 'all', '2022-11-19')
        all_tweet_count = len(c14response["data"])
        self.assertEqual(all_tweet_count, pos_tweet_count + neg_tweet_count + neu_tweet_count)

    def test_pie_chart_data(self):
        # check if correct data retrieved when no keyword input
        data = uD.show_all_tweets()
        data_list = data["data"]
        all_tweets_count = len(data_list)
        pc_list = uD.pie_chart_data()
        pc_tweets_count = pc_list[0] + pc_list[1] + pc_list[2]
        self.assertEqual(pc_tweets_count, all_tweets_count)

        # check if correct data retrieved when there is keyword input
        kw_data = uD.show_tweets_by_keyword('GE15')
        kw_data_list = kw_data["data"]
        kw_all_tweets_count = len(kw_data_list)
        kw_pc_list = uD.pie_chart_data('GE15')
        kw_pc_tweets_count = kw_pc_list[0] + kw_pc_list[1] + kw_pc_list[2]
        self.assertEqual(kw_pc_tweets_count, kw_all_tweets_count)

        # check if return list of [0, 0, 0] when no tweets matching keyword
        self.assertEqual(uD.pie_chart_data('scotland'), [0, 0, 0])

        # check if counts are categorised correctly based on sentiment based on sequence [pos, neu, neg]
        # categorisation of tweets into respective lists based on sentiment has already been tested previously,
        # so we assume that the length of list is the correct count of the sentiment tweets
        uD.show_all_tweets()
        pc = uD.pie_chart_data()

        self.assertEqual(len(uD.a_pos_list), pc[0])
        self.assertEqual(len(uD.a_neu_list), pc[1])
        self.assertEqual(len(uD.a_neg_list), pc[2])

        uD.show_tweets_by_keyword('GE15')
        pc1 = uD.pie_chart_data('GE15')

        self.assertEqual(len(uD.k_pos_list), pc1[0])
        self.assertEqual(len(uD.k_neu_list), pc1[1])
        self.assertEqual(len(uD.k_neg_list), pc1[2])

        # check if return type is correct (list)
        self.assertTrue(isinstance(uD.pie_chart_data(), list))
        # check if return type is correct (3 items in list only)
        self.assertTrue(len(uD.pie_chart_data()), 3)

    def test_line_chart_input(self):

        # check if correct data retrieved when no keyword input
        data = uD.show_all_tweets()
        data_list = data["data"]
        all_tweets_count = len(data_list)
        lc_list = uD.line_chart_input()

        final_tweet_count = 0
        for item in lc_list:
            tweet_count = item[1]
            final_tweet_count += tweet_count

        self.assertEqual(final_tweet_count, all_tweets_count)

        # check if correct data retrieved when there is keyword input
        kw_data = uD.show_tweets_by_keyword('GE15')
        kw_data_list = kw_data["data"]
        kw_all_tweets_count = len(kw_data_list)
        kw_lc_list = uD.line_chart_input('GE15')

        lc_final_tweet_count = 0
        for item in kw_lc_list:
            lc_tweet_count = item[1]
            lc_final_tweet_count += lc_tweet_count

        self.assertEqual(lc_final_tweet_count, kw_all_tweets_count)

        # check if return empty list when no tweets matching keyword
        self.assertEqual(uD.line_chart_input('scotland'), [])

        # sentiment tests

        # positive, total sum of values on different dates is the same as the total number of positive tweets
        # show_tweets_by_sentiment was tested previously so we assume the number of positive tweets is correct
        pos = uD.show_tweets_by_sentiment('GE15', 'positive')
        c1_list = pos["data"]
        all_pos_tweet_count = len(c1_list)
        c1_lc_list = uD.line_chart_input('GE15', 'positive')

        final_c1_tweet_count = 0
        for item in c1_lc_list:
            c1_tweet_count = item[1]
            final_c1_tweet_count += c1_tweet_count

        self.assertEqual(final_c1_tweet_count, all_pos_tweet_count)

        # no positive tweets
        c2response = uD.line_chart_input('goodbye', 'positive')
        self.assertEqual(c2response, [])

        # negative, total sum of values on different dates is the same as the total number of negative tweets
        # show_tweets_by_sentiment was tested previously so we assume the number of negative tweets is correct
        neg = uD.show_tweets_by_sentiment('GE15', 'negative')
        c2_list = neg["data"]
        all_neg_tweet_count = len(c2_list)
        c2_lc_list = uD.line_chart_input('GE15', 'negative')

        final_c2_tweet_count = 0
        for item in c2_lc_list:
            c2_tweet_count = item[1]
            final_c2_tweet_count += c2_tweet_count

        self.assertEqual(final_c2_tweet_count, all_neg_tweet_count)

        # no negative tweets
        c4response = uD.line_chart_input('goodbye', 'negative')
        self.assertEqual(c4response, [])

        # neutral, total sum of values on different dates is the same as the total number of neutral tweets
        # show_tweets_by_sentiment was tested previously so we assume the number of neutral tweets is correct
        neu = uD.show_tweets_by_sentiment('GE15', 'neutral')
        c3_list = neu["data"]
        all_neu_tweet_count = len(c3_list)
        c3_lc_list = uD.line_chart_input('GE15', 'neutral')

        final_c3_tweet_count = 0
        for item in c3_lc_list:
            c3_tweet_count = item[1]
            final_c3_tweet_count += c3_tweet_count

        self.assertEqual(final_c3_tweet_count, all_neu_tweet_count)

        # no neutral tweets
        c6response = uD.line_chart_input('good morning', 'neutral')
        self.assertEqual(c6response, [])

        # all sentiments, check if total number of tweets for all dates on the line chart same as
        # total number of tweets for that keyword
        # using tweet count returned by show tweets by keyword (tested previously)
        twt = uD.show_tweets_by_keyword('GE15')
        twt_count = len(twt["data"])
        c7response = uD.line_chart_input('GE15', 'all')
        final_c7_tweet_count = 0
        for item in c7response:
            c7_tweet_count = item[1]
            final_c7_tweet_count += c7_tweet_count

        self.assertEqual(final_c7_tweet_count, twt_count)

        # check if tweet count is correct for the date by using
        # show_tweets_by_sentiment (tested previously)
        # and comparing the tweet count with the count for the date in line chart input

        c8_data = uD.show_tweets_by_sentiment('GE15', 'positive', '2022-11-19')
        c8_count = len(c8_data["data"])

        c8response = uD.line_chart_input('GE15', 'positive')
        c8_lc_count = 0
        for item in c8response:
            if item[0] == "2022-11-19":
                c8_lc_count = item[1]

        self.assertEqual(c8_count, c8_lc_count)

    def test_show_word_frequency(self):

        # check if returns a response when keyword is empty
        self.assertNotEqual(uD.show_word_frequency('', 'all'), [])

        # check if returns a response when keyword is not empty
        self.assertNotEqual(uD.show_word_frequency('GE15', 'all'), [])

        # check if returns empty list when no tweets matching keyword
        self.assertEqual(uD.show_word_frequency('scotland'), [])

        # check if returns a response when there are tweets available for specified sentiment
        # check if returns empty list when there are no tweets available for specified sentiment

        # positive tweets
        self.assertNotEqual(uD.show_word_frequency('GE15', 'positive'), [])

        # no positive tweets
        self.assertEqual(uD.show_word_frequency('goodbye', 'positive'), [])

        # negative tweets
        self.assertNotEqual(uD.show_word_frequency('GE15', 'negative'), [])

        # no negative tweets
        self.assertEqual(uD.show_word_frequency('goodbye', 'negative'), [])

        # neutral tweets
        self.assertNotEqual(uD.show_word_frequency('GE15', 'neutral'), [])

        # no neutral tweets
        self.assertEqual(uD.show_word_frequency('good morning', 'neutral'), [])

        # check if word cloud input returns correct value for the word 'pru15'
        # by checking with the cleaned_text column for tweets with the keyword 'pru15'
        # then running the function to retrieve the frequency of 'pru15'

        response = uD.wc_show_tweets_by_keyword('pru15')
        response1 = response["data"]
        final_final_list = []
        for tweet in response1:
            list_of_words = str(tweet["cleaned_text"])
            words1 = list_of_words.strip('][')
            words = re.sub("[']", "", words1).split(', ')
            for word in words:
                final_final_list.append(word)

        counter = Counter(final_final_list)
        most_occur1 = counter.most_common(30)

        pru15_count = 0
        for i in most_occur1:
            if i[0] == 'pru15':
                pru15_count = i[1]

        wc_input = uD.show_word_frequency('pru15')
        wc_input_value = 0
        for item in wc_input:
            if item["text"] == "pru15":
                wc_input_value = item["value"]

        self.assertEqual(pru15_count, wc_input_value)


if __name__ == '__main__':
    unittest.main()
