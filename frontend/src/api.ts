import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || "http://localhost:8000/api",
  headers: {
    "X-API-Key": import.meta.env.VITE_API_KEY || "default-insecure-key",
  },
});

export default api;
