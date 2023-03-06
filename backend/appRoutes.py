from fastapi import FastAPI
import requests
import uvicorn
import getAndStoreTweets
import updateDashboard

# TODO: error handling

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAEdchgEAAAAAoMYohigl0ivRkDXA0Xbxm%2FC7BhM%3D2RV4sBsPfRtOfRRASXHrv50t0It6RGRDnXmHCusBNUgACJMu8q"

app = FastAPI()


@app.get("/sentiment-analysis")
async def sentiment_analysis(keyword):
    response = getAndStoreTweets.get_and_score_tweets(str(keyword))
    return response


@app.get("/show-all-tweets")
async def show_all_tweets(file='data/tweets_with_translations.csv'):
    response = updateDashboard.show_all_tweets(file)
    return response


@app.get("/show-tweets-by-sentiment")
async def show_tweets_by_sentiment(keyword='', sentiment='all'):
    response = updateDashboard.show_tweets_by_sentiment(str(keyword), str(sentiment))
    return response


@app.get("/show-tweets-by-keyword")
async def show_tweets_by_keyword(keyword):
    response = updateDashboard.show_tweets_by_keyword(str(keyword))
    return response


@app.get("/pie-chart")
async def pie_chart(keyword=''):
    response = updateDashboard.pie_chart_data(str(keyword))
    return response


@app.get("/word-cloud")
async def show_word_cloud(keyword='', sentiment='all'):
    response = updateDashboard.show_word_frequency(str(keyword), str(sentiment))
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)
