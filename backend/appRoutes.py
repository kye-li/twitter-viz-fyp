from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import updateDashboard

# TODO: error handling

app = FastAPI()

# ref: https://fastapi.tiangolo.com/tutorial/cors/

origins = [
    "http://localhost:3000/",
    "https://twitter-viz-fyp.vercel.app/",
    "https://f4b3-82-132-217-127.eu.ngrok.io/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/show-all-tweets")
async def show_all_tweets(file='data/tweets_with_translations.csv'):
    response = updateDashboard.show_all_tweets(file)
    return response


@app.get("/show-tweets-by-sentiment")
async def show_tweets_by_sentiment(keyword='', sentiment='all', date=''):
    response = updateDashboard.show_tweets_by_sentiment(str(keyword), str(sentiment), str(date))
    return response


@app.get("/show-tweets-by-keyword")
async def show_tweets_by_keyword(keyword):
    response = updateDashboard.show_tweets_by_keyword(str(keyword))
    return response


@app.get("/show-tweets-by-date")
async def show_tweets_by_date(date):
    response = updateDashboard.get_tweets_by_date(str(date))
    return response


@app.get("/pie-chart")
async def pie_chart(keyword=''):
    response = updateDashboard.pie_chart_data(str(keyword))
    return response


@app.get("/word-cloud")
async def show_word_cloud(keyword='', sentiment='all'):
    response = updateDashboard.show_word_frequency(str(keyword), str(sentiment))
    return response


@app.get("/line-chart")
async def show_line_chart(keyword='', sentiment='all'):
    response = updateDashboard.line_chart_input(str(keyword), str(sentiment))
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)
