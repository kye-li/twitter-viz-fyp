import WordCloud from "react-d3-cloud";
import { useCallback } from "react";

const Cloud = ({ wordCloudProp }) => {
    // part of css code from https://www.npmjs.com/package/react-d3-cloud
    return (
        <WordCloud data={wordCloudProp}
                   width={500}
                   height={200}
                   font="Times"
                   fontWeight="bold"
                   fontSize={useCallback((word) => Math.log2(word.value) * 5, [])}
        />
    )
};

export default Cloud;