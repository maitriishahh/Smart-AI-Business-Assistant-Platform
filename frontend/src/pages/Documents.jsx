import React, { useEffect, useState } from "react";
import API from "../api/axios";
import Sidebar from "../components/Sidebar";

export default function Documents() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    API.get("/admin/documents")
      .then((res) => {
        setDocuments(res.data.documents || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="flex bg-slate-950 min-h-screen">
      <Sidebar />
      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        <h1 className="text-3xl font-bold text-white mb-8">Documents</h1>
        {loading ? (
          <div className="text-white">Loading...</div>
        ) : documents.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {documents.map((doc) => (
              <div key={doc._id || doc.filename} className="bg-slate-800 rounded-2xl p-6 shadow flex flex-col">
                <div className="text-white font-semibold mb-2">{doc.filename}</div>
                <div className="text-slate-400 text-sm mb-2">Uploaded: {doc.uploaded_at ? new Date(doc.uploaded_at).toLocaleString() : "N/A"}</div>
                <div className="text-slate-300 text-xs truncate">Path: {doc.path}</div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-slate-400">No documents found.</div>
        )}
      </main>
    </div>
  );
}