import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Chat from "./pages/Chat";
import Analytics from "./pages/Analytics";
import Leads from "./pages/Leads";
import ChatLogs from "./pages/ChatLogs";
import Documents from "./pages/Documents";

function App() {

  const token = localStorage.getItem("token");

  return (

    <BrowserRouter>

      <Routes>

        {/* LOGIN */}

        <Route
          path="/login"
          element={<Login />}
        />

        {/* DASHBOARD */}

        <Route
          path="/dashboard"
          element={
            token
              ? <Dashboard />
              : <Navigate to="/login" />
          }
        />

        {/* CHAT */}

        <Route
          path="/chat"
          element={
            token
              ? <Chat />
              : <Navigate to="/login" />
          }
        />

        {/* ANALYTICS */}

        <Route
          path="/analytics"
          element={
            token
              ? <Analytics />
              : <Navigate to="/login" />
          }
        />

        {/* LEADS */}

        <Route
          path="/leads"
          element={
            token
              ? <Leads />
              : <Navigate to="/login" />
          }
        />

        {/* CHAT LOGS */}

        <Route
          path="/chat-logs"
          element={
            token
              ? <ChatLogs />
              : <Navigate to="/login" />
          }
        />

        {/* DOCUMENTS */}

        <Route
          path="/documents"
          element={
            token
              ? <Documents />
              : <Navigate to="/login" />
          }
        />

        {/* DEFAULT */}

        <Route
          path="*"
          element={
            <Navigate
              to={
                token
                  ? "/dashboard"
                  : "/login"
              }
            />
          }
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;