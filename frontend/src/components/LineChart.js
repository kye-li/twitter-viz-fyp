// all code below were written while learning and referring to documentation: https://www.chartjs.org/docs/latest/charts/line.html
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
        ],
    };

    return (<Line options={options} data={data} />);
};

export default LineChart;
