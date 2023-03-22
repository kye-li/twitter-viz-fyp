import {Box, Text} from "@chakra-ui/react";
import * as React from "react";

const TweetDisplay = ({ tweetDisplayProp }) => {

    const sentiment_text_colour = ( sentiment ) => {
        let colour;
        if (sentiment === "positive") {
            colour = 'red';
        } else if (sentiment === "negative") {
            colour = 'blue';
        } else {
            colour = 'darkgreen';
        }
        return colour;
    }

    // method to turn edit_history_tweet_ids into digits ['123456789'] to 123456789
    // pass it into the twitter url, allow user to click on link to view original tweet on twitter
    // e.g. https://twitter.com/anyuser/status/541278904204668929

    return (
        <div>
            {tweetDisplayProp?.data?.map((p, i) => (
                <Box marginTop="20px" key={i} border={"1px"} borderColor={"orchid"}>
                    {p.text}<Text fontWeight="bold" color={sentiment_text_colour(p.overall_sentiment)}> Sentiment: {p.overall_sentiment}</Text>
                    <Text fontWeight="bold"> Translation: {p.translation}</Text>
                </Box>
            ))}
        </div>
    );

};

export default TweetDisplay;