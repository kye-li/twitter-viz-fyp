import WordCloud from "react-d3-cloud";

const Cloud = ({ wordCloudProp }) => {
    // part of css code from https://www.npmjs.com/package/react-d3-cloud
    return (
        <WordCloud data={wordCloudProp}
                   width={500}
                   height={200}
                   font="Times"
                   fontWeight="bold"
                   fontSize={(word) => Math.log2(word.value) * 2}
        />
    )
};

export default Cloud;