import React, { useEffect, useState } from "react";
import API from "../api/axios";
import Sidebar from "../components/Sidebar";

export default function Leads() {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    API.get("/admin/leads")
      .then((res) => {
        setLeads(res.data.leads || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="flex bg-slate-950 min-h-screen">
      <Sidebar />
      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        <h1 className="text-3xl font-bold text-white mb-8">Leads</h1>
        {loading ? (
          <div className="text-white">Loading...</div>
        ) : leads.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-slate-800 rounded-2xl overflow-hidden">
              <thead>
                <tr>
                  <th className="px-6 py-3 text-left text-slate-400">Name</th>
                  <th className="px-6 py-3 text-left text-slate-400">Email</th>
                  <th className="px-6 py-3 text-left text-slate-400">Status</th>
                  <th className="px-6 py-3 text-left text-slate-400">Created</th>
                </tr>
              </thead>
              <tbody>
                {leads.map((lead) => (
                  <tr key={lead._id} className="hover:bg-slate-700 transition">
                    <td className="px-6 py-4 text-white">{lead.name}</td>
                    <td className="px-6 py-4 text-white">{lead.email}</td>
                    <td className="px-6 py-4 text-white">{lead.status}</td>
                    <td className="px-6 py-4 text-white">{new Date(lead.created_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-slate-400">No leads found.</div>
        )}
      </main>
    </div>
  );
}