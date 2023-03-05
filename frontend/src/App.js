import * as React from "react";
import {useState, useEffect} from "react";
import {Button, ChakraProvider, Container, Image, Text} from "@chakra-ui/react";
// import {ArcElement, Chart as ChartJS, Legend, Tooltip} from 'chart.js';
import './App.css';
import PieChart from "./components/PieChart";
import { SimpleGrid } from '@chakra-ui/react'
// ref: https://chakra-ui.com/docs/components/simple-grid/usage
import TweetDisplay from "./components/TweetDisplay";

function App() {
    // const [posts, setPosts] = useState({});
    const [sentimentTweets, setSentimentTweets] = useState({});
    // const [searchInput, setSearchInput] = useState("");
    const [pieChartData, setPieChartData] = useState([1, 1, 1]);
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


    // const enterSearch = (e) => {
    //     e.preventDefault();
    //     // alert(`The search value you entered was : ${searchInput}`);
    //     // getTweets({ query: `${searchInput}` });
    //     getTweetsWithSentiment({keyword: `${searchInput}`});
    //     updatePieChart({keyword: `${searchInput}`});
    // };
    //
    // const createWordCloud = () => {
    //     setWordCloud(ngrokURL + 'word-cloud?keyword=' + `${searchInput}`);
    //     alert('WordCloud will start loading after OK has been pressed. It may take up to 30 seconds.');
    // }
    //
    // const updateWordCloud = async ({keyword}) => {
    //     const response = await fetch(
    //         "/word-cloud?" +
    //         new URLSearchParams({
    //             keyword: keyword,
    //         })
    //     );
    //     if (!response.ok) {
    //         console.log("something messed up");
    //     } else {
    //         setWordCloud(ngrokURL + 'word-cloud?keyword=' + keyword);
    //         console.log(ngrokURL + 'word-cloud?keyword=' + keyword)
    //     }


        // useEffect(() => {
        //     fetchNgrokURL();
        // }, []);

        return (
            <ChakraProvider>
                <Text fontWeight="bold" textAlign="center" marginTop="20px">
                    Twitter Open Data Analyses and Visualisations 😊
                </Text>
                <SimpleGrid columns={2} spacing={2}>
                    <Container bg='lightgreen' height='50vh' width='100%'><Text>Hello</Text></Container>
                    <Container className='tweetsDisplay' bg='lightgreen' height='50vh' width='50vw'>
                        <Button onClick={() => getTweetsWithSentiment({sentiment: 'positive'})}>Show Positive Tweets</Button>
                        <Button onClick={() => getTweetsWithSentiment({sentiment: 'negative'})}>Show Negative Tweets</Button>
                        <Button onClick={() => getTweetsWithSentiment({sentiment: 'neutral'})}>Show Neutral Tweets</Button>
                        <Button onClick={() => getTweetsWithSentiment({sentiment: 'all'})}>Show All Tweets</Button>
                        <TweetDisplay tweetDisplayProp={sentimentTweets} />
                    </Container>

                    {/*<div className='rowA'>*/}
                {/*    <div className='searchBar'>*/}
                {/*    <form onSubmit={enterSearch}>*/}
                {/*        <label>Enter your search word here: </label>*/}
                {/*        <input*/}
                {/*            type="text"*/}
                {/*            value={searchInput}*/}
                {/*            onChange={(e) => setSearchInput(e.target.value)}*/}
                {/*        />*/}
                {/*        <input type="submit" name="search"/>*/}
                {/*    </form>*/}
                {/*    </div>*/}
                {/*</div>*/}
                {/*<div className='rowB'>*/}
                {/*    <Button onClick={() => createWordCloud()} >Load WordCloud</Button>*/}
                {/*    <Image src={wordCloud} />*/}
                {/*</div>*/}
                    <Container bg='lightgreen' height='50vh' width='100%'>
                        <PieChart pieChartProp={pieChartData}  />
                        <Button onClick={() => updatePieChart()} >Update Pie Chart</Button>
                    </Container>
                    <Container bg='lightgreen' height='50vh' width='50vw'><Text>Hello4</Text></Container>
                </SimpleGrid>
            </ChakraProvider>
           );
}


export default App;
