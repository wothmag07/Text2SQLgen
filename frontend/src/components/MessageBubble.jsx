import React, { useState } from "react";

export default function MessageBubble({ message }) {
  const [showSql, setShowSql] = useState(false);
  const isUser = message.role === "user";

  if (isUser) {
    return <div className="message user">{message.content}</div>;
  }

  const hasResults = message.columns?.length > 0 && message.results?.length > 0;
  const displayRows = message.results?.slice(0, 50);
  const totalRows = message.results?.length || 0;

  return (
    <div className="message assistant">
      <div className="response-text">{message.content}</div>

      {message.sql && (
        <div className="sql-block">
          <button className="sql-toggle" onClick={() => setShowSql(!showSql)}>
            {showSql ? "Hide SQL" : "Show SQL"}
          </button>
          {showSql && <pre className="sql-code">{message.sql}</pre>}
        </div>
      )}

      {hasResults && (
        <div className="results-table-wrapper">
          <table className="results-table">
            <thead>
              <tr>
                {message.columns.map((col, i) => (
                  <th key={i}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {displayRows.map((row, ri) => (
                <tr key={ri}>
                  {row.map((cell, ci) => (
                    <td key={ci}>{cell === null ? "NULL" : String(cell)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          {totalRows > 50 && (
            <div style={{ color: "#64748b", fontSize: "0.8rem", marginTop: "0.25rem" }}>
              Showing 50 of {totalRows} rows
            </div>
          )}
        </div>
      )}

      {message.error && <div className="error-text">{message.error}</div>}
    </div>
  );
}
