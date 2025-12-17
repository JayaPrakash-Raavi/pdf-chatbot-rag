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
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState("");

  async function send() {
    if (!question || !documentId) return;

    setMessages((m) => [...m, { role: "user", text: question }]);
    setQuestion("");

    const res = await askQuestion(documentId, question);
    setMessages((m) => [...m, { role: "ai", text: res.answer }]);
  }

  return (
    <div className="chat-page">
      <div className="chat-messages">
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            {m.text}
          </div>
        ))}
      </div>

      <div className="chat-input">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about the PDF..."
        />
        <button onClick={send}>Send</button>
      </div>
    </div>
  );
}
