"use client";

import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
);

export default function RateChart({ data }: any) {
  if (!data || data.length === 0) {
    return <p>No data available</p>;
  }

  const chartData = {
    labels: data.map((d: any) => d.effective_date),
    datasets: [
      {
        label: "Rates",
        data: data.map((d: any) =>
          d.rate_value === null ? null : d.rate_value
        ),
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
  };

  return (
    <div style={{ width: "100%", height: "300px" }}>
      <Line data={chartData} options={options} />
    </div>
  );
}
