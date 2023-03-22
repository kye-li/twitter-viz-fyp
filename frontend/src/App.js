import * as React from "react";
import {useState, useEffect} from "react";
import {Button, ChakraProvider, Container, Text} from "@chakra-ui/react";
// import {ArcElement, Chart as ChartJS, Legend, Tooltip} from 'chart.js';
import './App.css';
import PieChart from "./components/PieChart";
import { SimpleGrid } from '@chakra-ui/react'
// ref: https://chakra-ui.com/docs/components/simple-grid/usage
import TweetDisplay from "./components/TweetDisplay";
import WordCloud from "./components/WordCloud";
import LineChart from "./components/LineChart";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
// ref: https://reactdatepicker.com/

function App() {
    // const [posts, setPosts] = useState({});
    const [sentimentTweets, setSentimentTweets] = useState({});
    const [tweetDisplayText, setTweetDisplayText] = useState("Loading tweets...")
    const [searchInput, setSearchInput] = useState("");
    const [pieChartData, setPieChartData] = useState([]);
    const [wordCloudData, setWordCloudData] = useState([])
    const [pieChartStats, setPieChartStats] = useState("Loading pie chart...");
    const [searchText, setSearchText] = useState("Now showing dashboard for all tweets related " +
        "to Malaysia's 15th General Election.")
    const [topTenWords, setTopTenWords] = useState("Loading word cloud and top ten words display...")
    const [lineChartData, setLineChartData] = useState([]);
    const [lineChartStats, setLineChartStats] = useState('Loading line chart...');
    const [startDate, setStartDate] = useState(null);

    // making sure fetching from correct URL in production
    //ref: https://stackoverflow.com/questions/45847813/react-native-fetch-api-url-in-development-and-productive-mode

    const baseURL = process.env.NODE_ENV === 'development' ? '' : 'https://f4b3-82-132-217-127.eu.ngrok.io'
    const origin = process.env.NODE_ENV === 'development' ? 'http://localhost:3000' : 'https://twitter-viz-fyp.vercel.app/'
    const mode = process.env.NODE_ENV === 'development' ? "same-origin" : "cors"

    const showAllTweets = async () => {
        const response = await fetch(
            `${baseURL}/show-all-tweets`, {
                mode: mode,
                credentials: "include",
                method: "get",
                headers: new Headers({
                    "ngrok-skip-browser-warning": "69420",
                    "Origin": origin
                })
            });

        const data = await response.json();

        if (!response.ok) {
            console.log("something messed up");
        } else {
            setTweetDisplayText("Now showing all tweets in database.");
            setSentimentTweets(data);
            console.log(data)
        }
    };


    const updatePieChartByKeyword = async ({keyword}) => {
        const response = await fetch(
            `${baseURL}/pie-chart?` +
            new URLSearchParams({
                keyword: keyword,
            }), {
                mode: mode,
                credentials: "include",
                method: "get",
                headers: new Headers({
                    "ngrok-skip-browser-warning": "69420",
                    "Origin": origin
                })
            });

        const data = await response.json();


        if (!response.ok) {
            console.log("something messed up");
        } else {
            setPieChartData(data);
            console.log(data)
            let total, pos, neu, neg, posPer, neuPer, negPer, stats;
            total = data[0] + data[1] + data[2];
            pos = data[0];
            neu = data[1];
            neg = data[2];

            posPer = Math.round((pos/total)*100)
            neuPer = Math.round((neu/total)*100)
            negPer = Math.round((neg/total)*100)

            stats = "Now showing Pie Chart for keyword: "+ keyword + " -> Total tweets: " + String(total) + " | " + "\n"
                + "Positive: " + String(pos) + ", " + String(posPer) + "%" + " | " + "\n"
                + "Neutral: " + String(neu) + ", " + String(neuPer) + "%" + " | " + "\n"
                + "Negative: " + String(neg) + ", " + String(negPer) + "%";

            setPieChartStats(stats)
        }
    };


    const getTweetsWithSentiment = async (keyword, sentiment, date) => {

        if(date !== null){
            date = date.toISOString().split('T')[0];
        } else {
            date = '';
        }

        const response = await fetch(
            `${baseURL}/show-tweets-by-sentiment?` +
            new URLSearchParams({
                keyword: keyword,
                sentiment: sentiment,
                date: date,
            }), {
                mode: mode,
                credentials: "include",
                method: "get",
                headers: new Headers({
                    "ngrok-skip-browser-warning": "69420",
                    "Origin": origin
                })
            });

        const data = await response.json();

        if (!response.ok) {
            console.log("something messed up");
        } else if (data.length === 1) {
            if(date === '') {
                alert(data);
                setTweetDisplayText(data)
            }
            else {
                alert(data + " on this date: " + date);
                setTweetDisplayText(data + " on this date: " + date)
            }
            setSentimentTweets({})
        }
        else {
            setTweetDisplayText("Now showing " + sentiment + " tweets with keyword: " + keyword + ", on date: " + date)
            setSentimentTweets(data);
            console.log(data)
        }
    };

    const getTweetsByKeyword = async ({keyword}) => {
        const response = await fetch(
            `${baseURL}/show-tweets-by-keyword?` +
            new URLSearchParams({
                keyword: keyword,
            }), {
                mode: mode,
                credentials: "include",
                method: "get",
                headers: new Headers({
                    "ngrok-skip-browser-warning": "69420",
                    "Origin": origin
                })
            });

        const data = await response.json();

        if (!response.ok) {
            console.log("something messed up");
        } else if (typeof data === "string") {
            alert(data);
            setTweetDisplayText(data)
            setSentimentTweets({})
            setSearchText("Dashboard is empty as there is no match for tweets containing keyword. " +
                "Please enter a different keyword.")
            setLineChartStats("No match for tweets containing keyword. " +
            "Please enter a different keyword.")
            setTopTenWords("No match for tweets containing keyword. " +
                "Please enter a different keyword.")
        }
        else {
            setTweetDisplayText("Now showing tweets with the keyword: " + keyword)
            setSentimentTweets(data);
            console.log(data)
        }

    };

    const updateWordCloud = async (keyword, sentiment) => {
        const response = await fetch(
            `${baseURL}/word-cloud?` +
            new URLSearchParams({
                keyword: keyword,
                sentiment: sentiment
            }), {
                mode: mode,
                credentials: "include",
                method: "get",
                headers: new Headers({
                    "ngrok-skip-browser-warning": "69420",
                    "Origin": origin
                })
            });

        const data = await response.json();

        if (!response.ok) {
            console.log("something messed up");
        } else {
            setWordCloudData(data)
            console.log(data)
            if (data.length > 0) {
                let word;
                let size;
                let topTenString = '';
                for (let i = 0; i < 10; i++) {
                    word = data[i].text;
                    size = data[i].value;
                    topTenString += word + " (" + size + " times)" + ", ";
                }
                if (keyword === '') {
                    setTopTenWords("Top 10 words for " + sentiment + " tweets in the database " +
                        "are: " + "\n" + topTenString + ".");
                } else {
                    setTopTenWords("Top 10 words for " + sentiment + " tweets with the keyword: "
                        + keyword + " are: " + "\n" + topTenString + ".");
                }
            }
        }
    };


    const updateLineChart = async (keyword, sentiment) => {
        const response = await fetch(
            `${baseURL}/line-chart?` +
            new URLSearchParams({
                keyword: keyword,
                sentiment: sentiment
            }), {
                mode: mode,
                credentials: "include",
                method: "get",
                headers: new Headers({
                    "ngrok-skip-browser-warning": "69420",
                    "Origin": origin
                })
            });

        const data = await response.json();

        if (!response.ok) {
            console.log("something messed up");
        } else {
            setLineChartData(data);
            console.log(data)
            if (keyword === '') {
                setLineChartStats("Tweet counts by date for " + sentiment + " tweets in the database.");
            } else {
                setLineChartStats("Tweet counts by date for " + sentiment + " tweets with the keyword: "
                    + keyword + ".");
            }
        }
    };

    const enterSearch = (e) => {
        e.preventDefault();
        if (searchInput === '') {
            alert("Please enter a keyword to search.")
            setTweetDisplayText("Please enter a keyword to search.")
            setSentimentTweets({})
            setPieChartData([])
            setPieChartStats("Please enter a keyword to search.")
            setTopTenWords('Please enter a keyword to search.')
            setWordCloudData([])
            setSearchText("Dashboard is empty as no keyword is searched.")
            setLineChartData([])
        } else {
            let value;
            value = searchInput;
            setSearchText("Now showing dashboard for keyword: " + value);
            setTweetDisplayText("Loading tweets...");
            setSentimentTweets([]);
            setPieChartStats("Loading pie chart...");
            setPieChartData([]);
            setLineChartStats("Loading line chart...")
            setLineChartData([]);
            setTopTenWords("Loading word cloud and top ten words...");
            setWordCloudData([]);
            updatePieChartByKeyword({keyword: `${searchInput}`});
            console.log("enterSearch: updatepiechartbykeyword")
            updateLineChart(searchInput, 'all');
            console.log("enterSearch: updatelinechart")
            getTweetsByKeyword({keyword: `${searchInput}`});
            console.log("enterSearch: gettweetsbykeyword")
            updateWordCloud(searchInput,'all');
            console.log("enterSearch: updatewordcloud")
        }
    };

    const sentimentButton = (keyword, sentiment, date) => {
        setTweetDisplayText("Loading tweets...");
        setSentimentTweets([]);
        setLineChartStats("Loading line chart...");
        setLineChartData([]);
        setTopTenWords("Loading word cloud and top ten words display...");
        setWordCloudData([]);
        updateLineChart(keyword, sentiment)
        console.log("sentimentButton: updatelinechart")
        getTweetsWithSentiment(keyword, sentiment, date);
        console.log("sentimentButton: gettweetswithsentiment")
        updateWordCloud(keyword, sentiment);
        console.log("sentimentButton: updatewordcloud")
    };

    const resetButton = () => {
        setSearchInput('');
        setSearchText("Now showing dashboard for all tweets related to Malaysia's 15th General Election.");
        setStartDate(null);
        setTweetDisplayText("Loading tweets...");
        setSentimentTweets([]);
        setPieChartStats("Loading pie chart...");
        setPieChartData([]);
        setLineChartStats("Loading line chart...")
        setLineChartData([]);
        setTopTenWords("Loading word cloud and top ten words...");
        setWordCloudData([]);
        updatePieChartByKeyword({keyword: ''});
        console.log("reset: piechartupdate")
        updateLineChart('', 'all');
        console.log("reset: linechartupdate")
        updateWordCloud('','all');
        console.log("reset: wordcloudupdate")
        showAllTweets();
        console.log("reset: showalltweets")
    };

    useEffect(() => {
        updatePieChartByKeyword({keyword: ''});
        console.log("useEffect: piechartupdate")
        updateLineChart('', 'all');
        console.log("useEffect: linechartupdate")
        updateWordCloud('','all');
        console.log("useEffect: wordcloudupdate")
        showAllTweets();
        console.log("useEffect: showalltweets")
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
                            <Text fontWeight={"bold"} fontSize={"medium"} color={"brown"}>{pieChartStats}</Text>
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
                                    position={"sticky"}
                                    margin={"1"}
                                    borderColor={"black"}
                                    border={"1px"}
                                    onClick={() => sentimentButton(searchInput, 'positive', startDate)}
                            >
                                Show Positive Only
                            </Button>
                            <Button fontSize={"xs"}
                                    position={"sticky"}
                                    margin={"1"}
                                    borderColor={"black"}
                                    border={"1px"}
                                    onClick={() => sentimentButton(searchInput,'negative', startDate)}
                            >
                                Show Negative Only
                            </Button>
                            <Button fontSize={"xs"}
                                    position={"sticky"}
                                    margin={"1"}
                                    borderColor={"black"}
                                    border={"1px"}
                                    onClick={() => sentimentButton(searchInput,'neutral', startDate)}
                            >
                                Show Neutral Only
                            </Button>
                            {/*<Button fontSize={"xs"}*/}
                            {/*        position={"sticky"}*/}
                            {/*        onClick={() => showAllTweets()}*/}
                            {/*>*/}
                            {/*    Default Tweets*/}
                            {/*</Button>*/}
                            <Text fontWeight="bold">View Tweets by Date:</Text>
                            <DatePicker
                                showIcon
                                dateFormat="yyyy-MM-dd"
                                selected={startDate}
                                onChange={(date) => setStartDate(date)}
                                isClearable
                            />
                            <Button fontSize={"xs"}
                                    borderColor={"black"}
                                    border={"1px"}
                                    onClick={() => sentimentButton(searchInput,'all', startDate)}
                            >
                                Show All Tweets By Date
                            </Button>
                            <Button fontSize={"xs"}
                                    position={"sticky"}
                                    margin={"1"}
                                    borderColor={"black"}
                                    border={"1px"}
                                    backgroundColor={"deeppink"}
                                    textColor={"white"}
                                    onClick={() => resetButton()}
                            >
                                Reset Dashboard
                            </Button>
                            <Text fontWeight="bold" color={"brown"}>{tweetDisplayText}</Text>
                            <TweetDisplay tweetDisplayProp={sentimentTweets} />
                        </Container>
                        <Container bg="lavender" h="47vh" minW="100%" border="2px" overflow="scroll">
                            <Text fontWeight={"bold"} fontSize={"medium"} color={"brown"}>{lineChartStats}</Text>
                            <LineChart lineChartProp={lineChartData}/>
                        </Container>
                        <Container bg="lavender" h="47vh" minW="100%" overflow="scroll" border="2px">
                            <Text fontWeight={"bold"} color={"purple"} fontStyle={"italic"}>{topTenWords}</Text>
                            <WordCloud wordCloudProp={wordCloudData}/>
                        </Container>
                    </SimpleGrid>
                </Container>
            </ChakraProvider>
           );
}


export default App;
