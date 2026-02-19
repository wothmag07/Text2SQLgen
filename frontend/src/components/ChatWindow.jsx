import React, { useRef, useEffect } from "react";
import MessageBubble from "./MessageBubble";

export default function ChatWindow({ messages, loading }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="chat-window">
      {messages.length === 0 && !loading && (
        <div style={{ textAlign: "center", color: "#64748b", marginTop: "4rem" }}>
          Ask a question about your medical datasets to get started.
        </div>
      )}
      {messages.map((msg, i) => (
        <MessageBubble key={i} message={msg} />
      ))}
      {loading && (
        <div className="loading-indicator">
          Thinking<span className="loading-dots"></span>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}
