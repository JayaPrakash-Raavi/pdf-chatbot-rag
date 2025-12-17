import { useParams } from "react-router-dom";
import { useState } from "react";
import "./ChatPage.css";
import { askQuestion } from "../lib/api";

type Message = {
  role: "user" | "ai";
  text: string;
};

export default function ChatPage() {
  const { documentId } = useParams();
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);

  async function send() {
    if (!documentId || !question) return;

    setMessages((m) => [...m, { role: "user", text: question }]);
    setQuestion("");

    const res = await askQuestion(documentId, question);
    setMessages((m) => [...m, { role: "ai", text: res.answer }]);
  }

  return (
    <div className="chat-container">
      <h2>Resume Chat</h2>

      <div className="chat-box">
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.role}`}>
            {m.text}
          </div>
        ))}
      </div>

      <div className="input-row">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about this resume..."
        />
        <button onClick={send}>Send</button>
      </div>
    </div>
  );
}
