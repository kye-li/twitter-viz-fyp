import {Button, Text} from "@chakra-ui/react";
import * as React from "react";

const TweetDisplay = ({ tweetDisplayProp }) => {

    // const sentiment_text_colour = ({ sentiment }) => {
    //     let colour;
    //     console.log(sentiment)
    //     if (sentiment === "positive") {
    //         colour = 'red';
    //     } else if (sentiment === "negative") {
    //         colour = 'blue';
    //     } else {
    //         colour = 'yellow';
    //     }
    //     return colour;
    // }
    //
    // const bold_or_not = ({ alphabet }) => {
    //     let font;
    //     if(alphabet === 'a') {
    //         font = 'bold'
    //     } else {
    //         font = 'normal'
    //     }
    //     return font
    // }

    return (
        <div>
            {tweetDisplayProp?.data?.map((p, i) => (
                <Text marginTop="20px" key={i}>
                    {p.text}<Text fontWeight="bold" color="red"> Sentiment: {p.overall_sentiment}</Text>
                    <Text fontWeight="bold"> Translation: {p.translation}</Text>
                </Text>
            ))}
        </div>
    );

}

export default TweetDisplay;