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
    const [pieChartData, setPieChartData] = useState([]);
    const [wordCloudData, setWordCloudData] = useState([])
    const [pieChartStats, setPieChartStats] = useState("");
    const [searchText, setSearchText] = useState("Now showing dashboard for all tweets related " +
        "to Malaysia's 15th General Election.")
    const [topTenWords, setTopTenWords] = useState("")


    const showAllTweets = async () => {
        const response = await fetch(
            "/show-all-tweets", {
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


    const updatePieChartByKeyword = async ({keyword}) => {
        const response = await fetch(
            "/pie-chart?" +
            new URLSearchParams({
                keyword: keyword,
            }), {
                method: "get"
            });

        const data = await response.json()

        if (!response.ok) {
            console.log("something messed up");
        } else {
            setPieChartData(data);
            console.log(data)
            let total, pos, neu, neg, stats;
            total = data[0] + data[1] + data[2];
            pos = data[0];
            neu = data[1];
            neg = data[2];

            stats = "Total tweets: " + String(total) + "\n"
                + "Positive: " + String(pos) + "\n"
                + "Neutral: " + String(neu) + "\n"
                + "Negative: " + String(neg);
            setPieChartStats(stats)
        }
    };


    const getTweetsWithSentiment = async (keyword, sentiment) => {
        const response = await fetch(
            "/show-tweets-by-sentiment?" +
            new URLSearchParams({
                keyword: keyword,
                sentiment: sentiment,
            }), {
                method: "get"
            });

        const data = await response.json()

        if (!response.ok) {
            console.log("something messed up");
        } else if (data.length === 1) {
            alert(data);
        }
        else {
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
        } else if (typeof data === "string") {
            alert(data);
            setSearchText("Dashboard is empty as there is no match for tweets containing keyword. " +
                "Please enter a different keyword.")
        }
        else {
            setSentimentTweets(data);
            console.log(data)
        }

    };

    const updateWordCloud = async (keyword, sentiment) => {
        const response = await fetch(
            "/word-cloud?" +
            new URLSearchParams({
                keyword: keyword,
                sentiment: sentiment
            }), {
                method: "get"
            });

        const data = await response.json()

        if (!response.ok) {
            console.log("something messed up");
        } else {
            setWordCloudData(data)
            console.log(data)
            // data is an array of {text: '', value: }
            let word;
            let size;
            let topTenString = '';
            for(let i = 0; i < 10; i++){
                word = data[i].text;
                size = data[i].value;
                topTenString += word + " (" + size + " words)" + ", ";
            }
            if (keyword===''){
                setTopTenWords("Top 10 words for " + sentiment + " tweets in the database " +
                    "are: " + "\n" + topTenString + ".");
            }
            else {
                setTopTenWords("Top 10 words for " + sentiment + " tweets with the keyword: "
                    + keyword + " are: " + "\n" + topTenString + ".");
            }
        }
    };


    const enterSearch = (e) => {
        e.preventDefault();
        if (searchInput === '') {
            alert("Please enter a keyword to search.")
            setSentimentTweets({})
            setPieChartData([])
            setPieChartStats("")
            setWordCloudData([])
            setSearchText("Dashboard is empty as no keyword is searched.")
        } else {
            let value;
            value = searchInput;
            setSearchText("Now showing dashboard for keyword: " + value);
            // alert(`The search value you entered was : ${searchInput}`);
            // getTweets({ query: `${searchInput}` });
            getTweetsByKeyword({keyword: `${searchInput}`});
            updatePieChartByKeyword({keyword: `${searchInput}`});
            updateWordCloud(searchInput,'all');
        }
    };

    const sentimentButton = (keyword, sentiment) => {
        getTweetsWithSentiment(keyword, sentiment);
        updateWordCloud(keyword, sentiment);
    };

    useEffect(() => {
        updatePieChartByKeyword({keyword: ''});
        showAllTweets();
        updateWordCloud('','all')
    }, []);

        return (
            <ChakraProvider>
                <Container minH="100vh" minW="100vw" overflow="hidden" backgroundColor="purple">
                    <Text fontWeight="bold" textAlign="center" h="5vh" color="white" fontSize="large">
                        Twitter Open Data Analyses and Visualisations: A closer look into sentiments during Malaysia's 15th General Election
                    </Text>
                    <SimpleGrid columns={2} spacing={"0vh"} h="95vh" padding={1}>
                        <Container bg="lavender" h="47vh" minW="100%" border="2px" overflow="scroll">
                            <form onSubmit={enterSearch}>
                                <label><b>Enter your search word here: </b></label>
                                <input
                                    type="text"
                                    value={searchInput}
                                    onChange={(e) => setSearchInput(e.target.value)}
                                />
                                <input type="submit" />
                            </form>
                            <Text fontSize={"medium"} border={"2px"}>{searchText}</Text>
                            <Button fontSize={"xs"}
                                onClick={() =>updatePieChartByKeyword({keyword: ''})}
                            >
                                Default Pie Chart
                            </Button>
                            <Text fontWeight={"bold"} fontSize={"medium"}>{pieChartStats}</Text>
                            <PieChart pieChartProp={pieChartData} />
                        </Container>
                        <Container
                            className="tweetsDisplay"
                            bg="lavender"
                            h="47vh"
                            minW="100%"
                            border="2px"
                        >
                            <Button fontSize={"xs"}
                                onClick={() => sentimentButton(searchInput, 'positive')}
                            >
                                Show Positive Only
                            </Button>
                            <Button fontSize={"xs"}
                                onClick={() => sentimentButton(searchInput,'negative')}
                            >
                                Show Negative Only
                            </Button>
                            <Button fontSize={"xs"}
                                onClick={() => sentimentButton(searchInput,'neutral')}
                            >
                                Show Neutral Only
                            </Button>
                            <Button fontSize={"xs"}
                                onClick={() => sentimentButton(searchInput,'all')}
                            >
                                Show All
                            </Button>
                            <Button fontSize={"xs"}
                                onClick={() => showAllTweets()}
                            >
                                Default Tweets
                            </Button>
                            <TweetDisplay tweetDisplayProp={sentimentTweets} />
                        </Container>
                        <Container bg="lavender" h="47vh" minW="100%" border="2px" overflow="scroll">
                        </Container>
                        <Container bg="lavender" h="47vh" minW="100%" overflow="scroll" border="2px">
                            <Text fontWeight={"bold"} color={"purple"} fontStyle={"italic"}>{topTenWords}</Text>
                            <WordCloud wordCloudProp={wordCloudData}/>
                            {/*<Button*/}
                            {/*    onClick={() => updateWordCloud(`${searchInput}`)}*/}

                            {/*>*/}
                            {/*    Update Word Cloud*/}
                            {/*</Button>*/}
                            <Button fontSize={"xs"}
                                onClick={() => updateWordCloud('', 'all')}

                            >
                                Default Word Cloud
                            </Button>
                        </Container>
                    </SimpleGrid>
                </Container>
            </ChakraProvider>
           );
}


export default App;
