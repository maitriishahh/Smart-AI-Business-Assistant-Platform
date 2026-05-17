import React from "react";
import { NavLink } from "react-router-dom";

const navItems = [
  { name: "Dashboard", path: "/dashboard" },
  { name: "Analytics", path: "/analytics" },
  { name: "Leads", path: "/leads" },
  { name: "Chat Logs", path: "/chat-logs" },
  { name: "Documents", path: "/documents" },
];

export default function Sidebar() {
  return (
    <aside className="fixed top-0 left-0 h-full w-64 bg-slate-950 flex flex-col py-8 px-4 border-r border-slate-800 z-40">
      <div className="mb-10 flex items-center justify-center">
        <span className="text-2xl font-bold text-white tracking-wide">AI Biz Admin</span>
      </div>
      <nav className="flex flex-col gap-2">
        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `rounded-2xl px-5 py-3 text-lg font-medium transition-colors ${
                isActive
                  ? "bg-slate-800 text-white"
                  : "text-slate-300 hover:bg-slate-800 hover:text-white"
              }`
            }
            end
          >
            {item.name}
          </NavLink>
        ))}
      </nav>
      <div className="flex-grow" />
      <div className="text-xs text-slate-600 text-center pb-2">© {new Date().getFullYear()} AI Biz Platform</div>
    </aside>
  );
}