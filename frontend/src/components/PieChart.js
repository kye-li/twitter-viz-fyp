// ref: https://www.npmjs.com/package/react-minimal-pie-chart?activeTab=readme
// ref: https://react-chartjs-2.js.org/examples/pie-chart

// import { PieChart } from "react-minimal-pie-chart";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';

const PieChart = ({ pieChartProp }) => {
    // console.log(pieChartProp);
    ChartJS.register(ArcElement, Tooltip, Legend);

    const pie_data = {
        labels: ['Positive', 'Neutral', 'Negative'],
        datasets: [
            {
                label: '# of Tweets based on Sentiment',
                data: pieChartProp,
                backgroundColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 2)',
                    'rgba(255, 206, 86, 2)',
                    'rgba(54, 162, 235, 2)',
                ],
                borderWidth: 1,
            },
        ],
    };


    return (
        <Pie data={pie_data}/>
    );
};

export default PieChart;