import React, { useEffect, useState } from "react";
import API from "../api/axios";
import Sidebar from "../components/Sidebar";

export default function ChatLogs() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    API.get("/admin/chat-logs")
      .then((res) => {
        setLogs(res.data.logs || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="flex bg-slate-950 min-h-screen">
      <Sidebar />
      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        <h1 className="text-3xl font-bold text-white mb-8">Chat Logs</h1>
        {loading ? (
          <div className="text-white">Loading...</div>
        ) : logs.length > 0 ? (
          <div className="space-y-6">
            {logs.map((log) => (
              <div key={log._id} className="bg-slate-800 rounded-2xl p-6 shadow">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-slate-400 text-sm">{log.user_email}</span>
                  <span className="text-slate-500 text-xs">{new Date(log.timestamp).toLocaleString()}</span>
                </div>
                <div className="text-white font-semibold mb-1">User: {log.user}</div>
                <div className="text-slate-300">AI: {log.response}</div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-slate-400">No chat logs found.</div>
        )}
      </main>
    </div>
  );
}