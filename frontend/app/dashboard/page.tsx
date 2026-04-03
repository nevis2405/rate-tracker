"use client";

import { useEffect, useState } from "react";
import { getLatestRates, getHistoryRates } from "@/lib/api";
import RateTable from "@/components/RateTable";
import RateChart from "@/components/RateChart";

export default function Dashboard() {
  const [latest, setLatest] = useState<any[]>([]);
  const [history, setHistory] = useState<any[]>([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [provider, setProvider] = useState("");
  const [type, setType] = useState("");

  const loadData = async () => {
    try {
      const latestData = await getLatestRates();
      const historyData = await getHistoryRates({
        provider,
        type,
      });

      setLatest(latestData);
      setHistory(historyData.slice(0, 30));

      setError(null);
    } catch (err) {
      setError("Failed to fetch data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setLoading(true);
    loadData();

    const interval = setInterval(loadData, 60000);
    return () => clearInterval(interval);
  }, [provider, type]);

  return (
    <div
      style={{
        padding: "20px",
        maxWidth: "1000px",
        margin: "auto",
      }}
    >
      <h1 style={{textAlign:"center"}}><b>Rates Dashboard</b></h1>

      {/* FILTERS */}
      <div
        style={{
          marginBottom: "20px",
          display: "flex",
          gap: "10px",
          flexWrap: "wrap", // 🔥 mobile fix
        }}
      >
        <select value={provider} onChange={(e) => setProvider(e.target.value)}
          style={{border: "solid", marginRight:"10px"}}>
          <option value="">All Providers</option>
          <option value="Chase">Chase</option>
          <option value="HSBC">HSBC</option>
        </select>

        <select value={type} onChange={(e) => setType(e.target.value)}
          style={{border: "solid", marginRight:"10px"}}>
          <option value="">All Types</option>
          <option value="5yr_arm_mortgage">5yr ARM</option>
          <option value="30yr_fixed_mortgage">30yr Fixed</option>
        </select>
      </div>

      {/* Loading / Error INSIDE UI (better UX) */}
      {loading && <p>Loading rates...</p>}
      {error && <p>{error}</p>}

      {!loading && !error && (
        <>
          <h2><b>Trend</b></h2>
          <RateChart data={history} />
          <br/>
          <h2><b>Latest Rates</b></h2>
          <RateTable data={latest} />
        </>
      )}
    </div>
  );
}
