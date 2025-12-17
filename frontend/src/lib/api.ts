const API_BASE = import.meta.env.VITE_API_BASE;

export async function uploadPDF(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("PDF upload failed");
  }

  return res.json();
}

export async function askQuestion(
  documentId: string,
  question: string
) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      document_id: documentId,
      question,
    }),
  });

  if (!res.ok) {
    throw new Error("Chat request failed");
  }

  return res.json();
}
