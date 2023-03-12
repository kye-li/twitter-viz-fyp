// ref: https://www.chartjs.org/docs/latest/charts/line.html
import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

const LineChart = ({ lineChartProp }) => {
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const options = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top',
        },
        title: {
            display: true,
            // text: 'Tweet Counts by date',
        },
    },
};

// const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];

    const data = {
        // labels,
        datasets: [
            {
                label: 'Tweet Count',
                data: lineChartProp,
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)'
            }
            // {
            //     label: 'Dataset 2',
            //     data: [['Jan',700], ['Feb',600], ['Mar',500], ['Apr',400], ['May',300], ['Jun',200], ['Jul',100]],
            //     borderColor: 'rgb(53, 162, 235)',
            //     backgroundColor: 'rgba(53, 162, 235, 0.5)',
            // },
        ],
    };

    return (<Line options={options} data={data} />);
};

export default LineChart;