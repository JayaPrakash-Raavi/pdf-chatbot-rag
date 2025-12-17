import { useState } from "react";
import { uploadPDF } from "../lib/api";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [chatLink, setChatLink] = useState("");

  async function handleUpload() {
    if (!file) return;

    const res = await uploadPDF(file);
    const link = `${window.location.origin}/chat/${res.document_id}`;
    setChatLink(link);
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Hybrid Resume Chatbot</h1>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <button style={styles.button} onClick={handleUpload}>
        Upload PDF
      </button>

      {chatLink && (
        <div style={styles.linkBox}>
          <p>Your chatbot link:</p>
          <a href={chatLink}>{chatLink}</a>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    gap: "16px",
  },
  title: { fontSize: "28px", fontWeight: 700 },
  button: {
    padding: "10px 20px",
    background: "#4f46e5",
    color: "#fff",
    borderRadius: "6px",
  },
  linkBox: {
    marginTop: "20px",
    wordBreak: "break-all" as const,
  },
};
