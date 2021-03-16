const dev = {
  API_URL: "http://localhost:8000",
};

const prod = {
  API_URL: process.env.REACT_APP_API_URL,
};

const config = process.env.NODE_ENV === 'production'
  ? prod
  : dev;

export default {
  ...config
};
