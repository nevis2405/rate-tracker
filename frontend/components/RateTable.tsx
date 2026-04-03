"use client";

import { useState } from "react";

export default function RateTable({ data }: any) {
  const [sortKey, setSortKey] = useState("rate_value");
  const [order, setOrder] = useState("asc");

  const sortedData = [...data].sort((a, b) => {
    if (order === "asc") return a[sortKey] > b[sortKey] ? 1 : -1;
    return a[sortKey] < b[sortKey] ? 1 : -1;
  });

  return (
    <div style={{ overflowX: "auto" }}>
      {/* Sorting Controls */}
      <div style={{ marginBottom: "10px"}}>
        <button style={{ marginRight: "10px", border:"solid", padding:"5px"}} onClick={() => setSortKey("rate_value")}>
          Sort by Rate
        </button>
        <button style={{ marginRight: "10px", border:"solid", padding:"5px"}} onClick={() => setSortKey("effective_date")}>
          Sort by Date
        </button>
        <button style={{ marginRight: "10px", border:"solid", padding:"5px"}} onClick={() => setOrder(order === "asc" ? "desc" : "asc")}>
          Toggle Order
        </button>
      </div>

      <table
        style={{
          width: "100%",
          border: "1px solid #ccc",
          minWidth: "600px",
        }}
      >
        <thead>
          <tr>
            <th style={{ textAlign: "left" }}>Provider</th>
            <th style={{ textAlign: "left" }}>Type</th>
            <th style={{ textAlign: "left" }}>Rate</th>
            <th style={{ textAlign: "left" }}>Date</th>
          </tr>
        </thead>
        <tbody>
          {sortedData.map((row: any, i: number) => (
            <tr key={i}>
              <td>{row.provider}</td>
              <td>{row.rate_type}</td>
              <td>{row.rate_value}</td>
              <td>{row.effective_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
