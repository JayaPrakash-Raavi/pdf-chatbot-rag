const API_BASE = import.meta.env.VITE_API_BASE_URL;

export async function uploadPDF(file: File) {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: form,
  });

  return res.json();
}

export async function askQuestion(documentId: string, question: string) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ document_id: documentId, question }),
  });

  return res.json();
}
