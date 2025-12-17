import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./UploadPage.css";
import { uploadPDF } from "../lib/api";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const navigate = useNavigate();

  async function handleUpload() {
    if (!file) return;
    const res = await uploadPDF(file);
    navigate(`/chat/${res.document_id}`);
  }

  return (
    <div className="upload-page">
      <h1>Hybrid Resume Chatbot</h1>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <button onClick={handleUpload}>Upload PDF</button>
    </div>
  );
}
