import axios from "axios";
import config from "../config";

export const API_URL = config.API_URL;

export const baseAPI = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-type": "application/json"
  }
});

