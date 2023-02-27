from fastapi import FastAPI
import requests
import uvicorn
import getAndStoreTweets
from fastapi.responses import FileResponse

# TODO: error handling

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAEdchgEAAAAAoMYohigl0ivRkDXA0Xbxm%2FC7BhM%3D2RV4sBsPfRtOfRRASXHrv50t0It6RGRDnXmHCusBNUgACJMu8q"

app = FastAPI()


# test endpoint
@app.get("/test")
async def test():
    return {"message": "Hello World"}


@app.get("/search-recent")
async def search_twitter(query):
    headers = {"Authorization": "Bearer {}".format(BEARER_TOKEN)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={}".format(
        query
    )
    # insert keyword/hastag in url
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


@app.get("/sentiment-analysis")
async def sentiment_analysis(keyword):
    response = getAndStoreTweets.get_and_score_tweets(str(keyword))
    return response


@app.get("/pie-chart")
async def pie_chart(keyword):
    response = getAndStoreTweets.get_pie_data(str(keyword))
    return response


@app.get("/word-cloud")
async def show_word_cloud(keyword):
    getAndStoreTweets.get_wordcloud(str(keyword))
    return FileResponse("../wc.png")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)

