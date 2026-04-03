import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/rates",
});

export const getLatestRates = async () => {
  const res = await API.get("/latest/");
  return res.data;
};

export const getHistoryRates = async (params?: {
  provider?: string;
  type?: string;
}) => {
  const res = await API.get("/history/", { params });
  return res.data;
};
