import React, { useState, useEffect } from "react";
import ChatWindow from "./components/ChatWindow";
import InputBar from "./components/InputBar";
import Suggestions from "./components/Suggestions";
import { sendMessage, fetchSuggestions } from "./api/chat";
import "./App.css";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    fetchSuggestions()
      .then(setSuggestions)
      .catch(() => {});
  }, []);

  const handleSend = async (text) => {
    if (!text.trim() || loading) return;

    const userMsg = { role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const history = messages
        .reduce((acc, msg, i, arr) => {
          if (msg.role === "user" && arr[i + 1]?.role === "assistant") {
            acc.push([msg.content, arr[i + 1].content]);
          }
          return acc;
        }, []);

      const data = await sendMessage(text, history);
      const assistantMsg = {
        role: "assistant",
        content: data.response,
        sql: data.sql,
        columns: data.columns,
        results: data.results,
        error: data.error,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Failed to get a response. Is the backend running?",
          error: err.message,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Text2SQL Agent</h1>
        <p>Ask questions about medical datasets in natural language</p>
      </header>
      <ChatWindow messages={messages} loading={loading} />
      {messages.length === 0 && (
        <Suggestions suggestions={suggestions} onSelect={handleSend} />
      )}
      <InputBar onSend={handleSend} disabled={loading} />
    </div>
  );
}
