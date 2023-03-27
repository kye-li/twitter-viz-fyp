from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import updateDashboard

# https://fastapi.tiangolo.com/tutorial/first-steps/

app = FastAPI()  # this line of code was taken from the FastAPI tutorial linked above

# origins and app.add_middleware() code below taken from reference https://fastapi.tiangolo.com/tutorial/cors/

origins = [  
    "http://127.0.0.1:5049",
    "http://127.0.0.1:5049/",
    "http://localhost:3000",
    "http://localhost:3000/",
    "http://localhost:8080",
    "http://localhost:8080/",
    "https://twitter-viz-fyp.vercel.app",
    "https://twitter-viz-fyp.vercel.app/"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/tutorial/first-steps/
# the app.get() methods were written while learning from the tutorial linked above


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

# https://www.uvicorn.org/#uvicornrun
# https://www.tutorialspoint.com/fastapi/fastapi_uvicorn.htm
# the code below was taken from the tutorials mentioned above 

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)
