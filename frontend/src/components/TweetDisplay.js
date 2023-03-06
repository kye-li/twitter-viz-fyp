import {Button, Text} from "@chakra-ui/react";
import * as React from "react";

const TweetDisplay = ({ tweetDisplayProp }) => {

    const sentiment_text_colour = ( sentiment ) => {
        let colour;
        console.log(sentiment)
        if (sentiment === "positive") {
            colour = 'red';
        } else if (sentiment === "negative") {
            colour = 'blue';
        } else {
            colour = 'darkgreen';
        }
        return colour;
    }

    return (
        <div>
            {tweetDisplayProp?.data?.map((p, i) => (
                <Text marginTop="20px" key={i}>
                    {p.text}<Text fontWeight="bold" color={sentiment_text_colour(p.overall_sentiment)}> Sentiment: {p.overall_sentiment}</Text>
                    <Text fontWeight="bold"> Translation: {p.translation}</Text>
                </Text>
            ))}
        </div>
    );

}

export default TweetDisplay;