import React from "react";

export default function Suggestions({ suggestions, onSelect }) {
  if (!suggestions || suggestions.length === 0) return null;

  return (
    <div className="suggestions">
      {suggestions.map((text, i) => (
        <button key={i} onClick={() => onSelect(text)}>
          {text}
        </button>
      ))}
    </div>
  );
}
