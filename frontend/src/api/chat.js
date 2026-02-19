import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "";

export async function sendMessage(message, history) {
  const res = await axios.post(`${API_BASE}/api/chat`, { message, history });
  return res.data;
}

export async function fetchSuggestions() {
  const res = await axios.get(`${API_BASE}/api/suggestions`);
  return res.data.suggestions;
}

export async function fetchSchema() {
  const res = await axios.get(`${API_BASE}/api/schema`);
  return res.data.schema;
}
