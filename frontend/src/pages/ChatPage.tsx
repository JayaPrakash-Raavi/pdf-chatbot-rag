import { useParams } from "react-router-dom";
import { useState } from "react";
import { askQuestion } from "../lib/api";

export default function ChatPage() {
  const { documentId } = useParams();
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<
    { role: "user" | "ai"; text: string }[]
  >([]);

  async function send() {
    if (!question || !documentId) return;

    setMessages((m) => [...m, { role: "user", text: question }]);
    setQuestion("");

    const res = await askQuestion(documentId, question);
    setMessages((m) => [...m, { role: "ai", text: res.answer }]);
  }

  return (
    <div style={styles.container}>
      <h2>Resume Chatbot</h2>

      <div style={styles.chat}>
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              ...styles.msg,
              alignSelf: m.role === "user" ? "flex-end" : "flex-start",
              background: m.role === "user" ? "#e5e7eb" : "#c7d2fe",
            }}
          >
            {m.text}
          </div>
        ))}
      </div>

      <div style={styles.inputRow}>
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about this resume..."
          style={styles.input}
        />
        <button onClick={send}>Send</button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    padding: "20px",
    display: "flex",
    flexDirection: "column",
  },
  chat: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    overflowY: "auto" as const,
  },
  msg: {
    padding: "10px",
    borderRadius: "8px",
    maxWidth: "70%",
  },
  inputRow: {
    display: "flex",
    gap: "8px",
  },
  input: {
    flex: 1,
    padding: "10px",
  },
};
