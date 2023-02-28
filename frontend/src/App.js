import * as React from "react";
import {useState, useEffect} from "react";
import {Button, ChakraProvider, Image, Text} from "@chakra-ui/react";
import {ArcElement, Chart as ChartJS, Legend, Tooltip} from 'chart.js';
import {Pie} from 'react-chartjs-2';
import './App.css';

function App() {
    // const [message, setMessage] = useState("");
    // const [posts, setPosts] = useState({});
    const [sentimentTweets, setSentimentTweets] = useState({});
    const [searchInput, setSearchInput] = useState("");
    const [pieChartData, setPieChartData] = useState([1, 1, 1]);
    const ngrokURL = process.env.REACT_APP_NGROK_BASE_URL;
    const [wordCloud, setWordCloud] = useState('https://about.twitter.com/content/dam/about-twitter/en/brand-toolkit/brand-download-img-1.jpg.twimg.1920.jpg')

    ChartJS.register(ArcElement, Tooltip, Legend);

    const pie_data = {
        labels: ['Negative', 'Neutral', 'Positive'],
        datasets: [
            {
                label: '# of Votes',
                data: pieChartData,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                ],
                borderWidth: 1,
            },
        ],
    };

    // const getWelcomeMessage = async () => {
    //   const requestOptions = {
    //     method: "GET",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //   };
    //   const response = await fetch("/test", requestOptions);
    //   const data = await response.json();
    //
    //   if (!response.ok) {
    //     console.log("something messed up");
    //   } else {
    //     setMessage(data.message);
    //   }
    // };

    // const getTweets = async ({ query }) => {
    //   const response = await fetch(
    //     "/search-recent?" +
    //       new URLSearchParams({
    //         query: query,
    //       })
    //   );
    //   const data = await response.json();
    //
    //   if (!response.ok) {
    //     console.log("something messed up");
    //   } else {
    //     setPosts(data);
    //   }
    // };

    const getTweetsWithSentiment = async ({keyword}) => {
        const response = await fetch(
            "/sentiment-analysis?" +
            new URLSearchParams({
                keyword: keyword,
            }), {
                method: "get",
                headers: new Headers({
                    "ngrok-skip-browser-warning": "69420",
                }),
            });

        const data = await response.json()

        if (!response.ok) {
            console.log("something messed up");
        } else {
            setSentimentTweets(data);
            console.log(data)
        }
    };

    const enterSearch = (e) => {
        e.preventDefault();
        // alert(`The search value you entered was : ${searchInput}`);
        // getTweets({ query: `${searchInput}` });
        getTweetsWithSentiment({keyword: `${searchInput}`});
        updatePieChart({keyword: `${searchInput}`});
    };

    const updatePieChart = async ({keyword}) => {
        const response = await fetch(
            "/pie-chart?" +
            new URLSearchParams({
                keyword: keyword,
            }),{
                method: "get",
                headers: new Headers({
                    "ngrok-skip-browser-warning": "69420",
                }),
            });

        const data = await response.json()

        if (!response.ok) {
            console.log("something messed up");
        } else {
            setPieChartData(data);
            console.log(data)
        }
    };

    const createWordCloud = () => {
        setWordCloud(ngrokURL + 'word-cloud?keyword=' + `${searchInput}`);
        alert('WordCloud will start loading after OK has been pressed. It may take up to 30 seconds.');
    }

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
                <div className='rowA'>
                    <div className='searchBar'>
                    <form onSubmit={enterSearch}>
                        <label>Enter your search word here: </label>
                        <input
                            type="text"
                            value={searchInput}
                            onChange={(e) => setSearchInput(e.target.value)}
                        />
                        <input type="submit" name="search"/>
                    </form>
                    </div>
                {/*<Text fontWeight="bold" textAlign="center" marginTop="20px">*/}
                {/*  This message is from the API: {message}*/}
                {/*</Text>*/}
                    <div className='tweetsDisplay'>
                    <Button onClick={() => getTweetsWithSentiment({keyword: `${searchInput}`})}>More Tweets</Button>
                    {sentimentTweets?.data?.map((p, i) => (
                        <Text marginTop="20px" key={i}>
                            {p.text} <b>Sentiment: {p.sentiment}</b>
                        </Text>
                    ))}
                    </div>
                </div>
                <div className='rowB'>
                    <Pie data={pie_data}/>
                    <Button onClick={() => createWordCloud()} >Load WordCloud</Button>
                    <Image src={wordCloud} />
                </div>
            </ChakraProvider>
        );
}


export default App;
