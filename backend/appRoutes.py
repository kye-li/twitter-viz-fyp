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


@app.get("/show-tweets")
async def show_tweets(sentiment):
    response = updateDashboard.show_tweets(str(sentiment))
    return response


@app.get("/show-tweets-by-keyword")
async def show_tweets_by_keyword(keyword):
    response = updateDashboard.show_tweets_by_keyword(keyword)
    return response


@app.get("/pie-chart")
async def pie_chart():
    response = updateDashboard.pie_chart_data('data/tweets_with_translations.csv')
    return response


@app.get("/word-cloud")
async def show_word_cloud():
    response = updateDashboard.show_word_frequency('data/tweets_with_translations.csv')
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)
