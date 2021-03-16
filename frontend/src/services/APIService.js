import axios from "axios";
import config from "../config";

export const API_URL = config.API_URL;
export const token = localStorage.getItem("token")

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-type": "application/json",
    "Authorization": `${token ? ("Token " + token) : ""}`
  }
});

api.interceptors.request.use(
  async (config) => {
    const token = localStorage.getItem("token");

    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return Promise.resolve(config);
  }
);

api.interceptors.response.use(response => {
    return response
  }, error => {
    if (error.response.status === 401) {
      window.location = '/auth/login/'
    }

    return Promise.reject(error);
  }
)
