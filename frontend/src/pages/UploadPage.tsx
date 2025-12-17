import { useState } from "react";
import "./UploadPage.css";
import { uploadPDF } from "../lib/api";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [link, setLink] = useState("");

  async function handleUpload() {
    if (!file) return;
    const res = await uploadPDF(file);
    setLink(`${window.location.origin}/chat/${res.document_id}`);
  }

  return (
    <div className="upload-container">
      <h1>Hybrid Resume Chatbot</h1>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <button onClick={handleUpload}>Upload PDF</button>

      {link && (
        <div className="share-box">
          <p>Share this link:</p>
          <a href={link}>{link}</a>
        </div>
      )}
    </div>
  );
}
