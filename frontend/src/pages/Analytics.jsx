import React, { useEffect, useState } from "react";
import API from "../api/axios";
import Sidebar from "../components/Sidebar";

export default function Analytics() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    API.get("/admin/analytics")
      .then((res) => {
        setMetrics(res.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="flex bg-slate-950 min-h-screen">
      <Sidebar />
      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        <h1 className="text-3xl font-bold text-white mb-8">Analytics</h1>
        {loading ? (
          <div className="text-white">Loading...</div>
        ) : metrics ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-slate-800 rounded-2xl p-8 shadow">
              <div className="text-slate-400 mb-2">Total Leads</div>
              <div className="text-3xl font-bold text-white">{metrics.total_leads}</div>
            </div>
            <div className="bg-slate-800 rounded-2xl p-8 shadow">
              <div className="text-slate-400 mb-2">Total Conversations</div>
              <div className="text-3xl font-bold text-white">{metrics.total_conversations}</div>
            </div>
            <div className="bg-slate-800 rounded-2xl p-8 shadow">
              <div className="text-slate-400 mb-2">Uploaded Documents</div>
              <div className="text-3xl font-bold text-white">{metrics.total_documents}</div>
            </div>
            <div className="bg-slate-800 rounded-2xl p-8 shadow">
              <div className="text-slate-400 mb-2">CRM Syncs</div>
              <div className="text-3xl font-bold text-white">{metrics.crm_syncs}</div>
            </div>
            <div className="bg-slate-800 rounded-2xl p-8 shadow">
              <div className="text-slate-400 mb-2">Automations Run</div>
              <div className="text-3xl font-bold text-white">{metrics.automations_run}</div>
            </div>
            {/* Add more cards as needed */}
          </div>
        ) : (
          <div className="text-red-400">Failed to load analytics.</div>
        )}
      </main>
    </div>
  );
}