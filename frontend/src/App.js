import * as React from "react";
import {useState, useEffect} from "react";
import {Button, ChakraProvider, Container, Image, Text} from "@chakra-ui/react";
// import {ArcElement, Chart as ChartJS, Legend, Tooltip} from 'chart.js';
import './App.css';
import PieChart from "./components/PieChart";
import { SimpleGrid } from '@chakra-ui/react'
// ref: https://chakra-ui.com/docs/components/simple-grid/usage
import TweetDisplay from "./components/TweetDisplay";
import WordCloud from "./components/WordCloud";

function App() {
    // const [posts, setPosts] = useState({});
    const [sentimentTweets, setSentimentTweets] = useState({});
    const [searchInput, setSearchInput] = useState("");
    const [pieChartData, setPieChartData] = useState([1, 1, 1]);
    const [wordCloudData, setWordCloudData] = useState([])
    // const ngrokURL = process.env.REACT_APP_NGROK_BASE_URL;
    // const [wordCloud, setWordCloud] = useState('https://about.twitter.com/content/dam/about-twitter/en/brand-toolkit/brand-download-img-1.jpg.twimg.1920.jpg')

    // ChartJS.register(ArcElement, Tooltip, Legend);

    const updatePieChart = async () => {
        const response = await fetch(
            "/pie-chart?" +
            {
                method: "get"
            });

        const data = await response.json()

        if (!response.ok) {
            console.log("something messed up");
        } else {
            setPieChartData(data);
            console.log(data)
        }
    };

    const getTweetsWithSentiment = async ({sentiment}) => {
        const response = await fetch(
            "/show-tweets?" +
            new URLSearchParams({
                sentiment: sentiment,
            }), {
                method: "get"
            });

        const data = await response.json()

        if (!response.ok) {
            console.log("something messed up");
        } else {
            setSentimentTweets(data);
            console.log(data)
        }
    };

    const getTweetsByKeyword = async ({keyword}) => {
        const response = await fetch(
            "/show-tweets-by-keyword?" +
            new URLSearchParams({
                keyword: keyword,
            }), {
                method: "get"
            });

        const data = await response.json()

        if (!response.ok) {
            console.log("something messed up");
        } else {
            setSentimentTweets(data);
            console.log(data)
        }

        if (data === "No match, please enter a different keyword.") {
            alert(data)
        }

    };



    const enterSearch = (e) => {
        e.preventDefault();
        // alert(`The search value you entered was : ${searchInput}`);
        // getTweets({ query: `${searchInput}` });
        getTweetsByKeyword({keyword: `${searchInput}`});
        // updatePieChart({keyword: `${searchInput}`});
    };


    const updateWordCloud = async () => {
        const response = await fetch(
            "/word-cloud"
        );

        const data = await response.json()

        if (!response.ok) {
            console.log("something messed up");
        } else {
            setWordCloudData(data)
            console.log(data)
        }
    };


        // useEffect(() => {
        //     fetchNgrokURL();
        // }, []);

        return (
            <ChakraProvider>
                <Container minH="100vh" minW="100vw" overflow="hidden">
                    <Text fontWeight="bold" textAlign="center" h="5vh">
                        Twitter Open Data Analyses and Visualisations 😊
                    </Text>
                    <SimpleGrid columns={2} spacing={"1vh"} h="95vh">
                        <Container bg="lightgreen" h="47vh" minW="100%">
                            <form onSubmit={enterSearch}>
                                <label>Enter your search word here: </label>
                                <input
                                    type="text"
                                    value={searchInput}
                                    onChange={(e) => setSearchInput(e.target.value)}
                                />
                                <input type="submit" name="search"/>
                            </form>
                        </Container>
                        <Container
                            className="tweetsDisplay"
                            bg="lightgreen"
                            h="47vh"
                            minW="100%"
                        >
                            <Button
                                onClick={() => getTweetsWithSentiment({sentiment: 'positive'})}
                            >
                                Show Positive Tweets
                            </Button>
                            <Button
                                onClick={() => getTweetsWithSentiment({sentiment: 'negative'})}
                            >
                                Show Negative Tweets
                            </Button>
                            <Button
                                onClick={() => getTweetsWithSentiment({sentiment: 'neutral'})}
                            >
                                Show Neutral Tweets
                            </Button>
                            <Button
                                onClick={() => getTweetsWithSentiment({sentiment: 'all'})}
                            >
                                Show All Tweets
                            </Button>
                            <TweetDisplay tweetDisplayProp={sentimentTweets} />
                        </Container>
                        <Container bg="lightgreen" h="47vh" minW="100%" overflow="scroll">
                            <Button
                                onClick={() => updatePieChart()}
                            >
                                Update Pie Chart
                            </Button>
                            <PieChart pieChartProp={pieChartData}  />
                        </Container>
                        <Container bg="lightgreen" h="47vh" minW="100%">
                            <WordCloud wordCloudProp={wordCloudData}/>
                            <Button
                                onClick={() => updateWordCloud()}

                            >
                                Update Word Cloud
                            </Button>
                        </Container>
                    </SimpleGrid>
                </Container>
            </ChakraProvider>
           );
}


export default App;
