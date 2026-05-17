import { Link } from "react-router-dom";

import {
  LayoutDashboard,
  MessageSquare
} from "lucide-react";

function Sidebar() {

  return (

    <div className="
      w-64
      min-h-screen
      bg-slate-900
      p-5
      border-r
      border-slate-700
      text-white
    ">

      {/* Logo */}

      <h1 className="
        text-3xl
        font-bold
        mb-10
        text-blue-400
      ">
        AI Assistant
      </h1>



      {/* Navigation */}

      <div className="flex flex-col gap-4">

        {/* Dashboard */}

        <Link
          to="/dashboard"
          className="
            flex
            items-center
            gap-3
            p-3
            rounded-xl
            hover:bg-slate-700
            transition
          "
        >
          <LayoutDashboard size={20} />

          <span>
            Dashboard
          </span>

        </Link>



        {/* Chat */}

        <Link
          to="/chat"
          className="
            flex
            items-center
            gap-3
            p-3
            rounded-xl
            hover:bg-slate-700
            transition
          "
        >
          <MessageSquare size={20} />

          <span>
            Chat
          </span>

        </Link>

      </div>



      {/* Bottom Section */}

      <div className="absolute bottom-6 left-5 text-sm text-slate-400">

        Smart AI Business Platform

      </div>

    </div>
  );
}

export default Sidebar;