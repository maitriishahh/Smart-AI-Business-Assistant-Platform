import {
  useState,
  useEffect,
  useRef
} from "react";

import Sidebar from "../components/Sidebar";
import API from "../api/axios";

import ReactMarkdown from "react-markdown";

function Chat() {

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // Upload Status
  const [uploadStatus, setUploadStatus] = useState("");

  const messagesEndRef = useRef(null);



  // =========================================
  // Auto Scroll
  // =========================================

  useEffect(() => {

    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth"
    });

  }, [messages]);



  // =========================================
  // Upload File
  // =========================================

  const uploadFile = async (e) => {

    const file = e.target.files[0];

    if (!file) return;

    const formData = new FormData();

    formData.append("file", file);

    try {

      await API.post(
        "/upload/pdf",
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data"
          }
        }
      );

      // Upload Notification
      setUploadStatus(
        `PDF "${file.name}" uploaded successfully`
      );

      setTimeout(() => {
        setUploadStatus("");
      }, 3000);

      e.target.value = null;

    } catch (error) {

      console.log(error);

      alert("Upload Failed");
    }
  };



  // =========================================
  // Send Message
  // =========================================

  const sendMessage = async () => {

    if (!message.trim()) return;

    const userMessage = {
      role: "user",
      text: message
    };

    setMessages((prev) => [
      ...prev,
      userMessage
    ]);

    setLoading(true);

    try {

      const response = await API.post(
        "/chat/query",
        {
          message,
          session_id: "frontend_session"
        }
      );

      const aiMessage = {
        role: "ai",
        text: response.data.response
      };

      setMessages((prev) => [
        ...prev,
        aiMessage
      ]);

      setMessage("");

    } catch (error) {

      console.log(error.response);

      alert(
        error.response?.data?.detail ||
        "Chat Error"
      );

    } finally {

      setLoading(false);
    }
  };



  // =========================================
  // UI
  // =========================================

  return (

    <div className="flex bg-slate-950 min-h-screen text-white">

      {/* Sidebar */}
      <Sidebar />



      {/* Main Content */}
      <main className="
        flex-1
        ml-64
        p-8
        flex
        flex-col
        h-screen
      ">

        {/* Header */}

        <h1 className="
          text-4xl
          font-bold
          mb-6
        ">
          AI Chat Assistant
        </h1>



        {/* Upload Section */}

        <div className="
          bg-slate-800
          p-5
          rounded-2xl
          shadow-lg
          mb-5
        ">

          <h2 className="
            text-xl
            font-semibold
            mb-4
          ">
            Upload PDF for RAG
          </h2>

          <input
            type="file"
            accept=".pdf"
            onChange={uploadFile}
            className="
              bg-slate-700
              p-3
              rounded-xl
              cursor-pointer
              w-full
            "
          />



          {/* Upload Status */}

          {uploadStatus && (

            <p className="
              text-green-400
              mt-3
              text-sm
            ">
              {uploadStatus}
            </p>

          )}

        </div>



        {/* Chat Messages */}

        <div className="
          flex-1
          bg-slate-800
          rounded-2xl
          p-6
          overflow-y-auto
          shadow-lg
        ">

          {messages.map((msg, index) => (

            <div
              key={index}
              className={`
                mb-6
                flex
                flex-col
                ${
                  msg.role === "user"
                    ? "items-end"
                    : "items-start"
                }
              `}
            >

              {/* Label */}

              <span className="
                text-sm
                text-slate-400
                mb-1
              ">
                {
                  msg.role === "user"
                    ? "You"
                    : "AI Assistant"
                }
              </span>



              {/* Bubble */}

              <div
                className={`
                  p-4
                  rounded-2xl
                  max-w-3xl
                  whitespace-pre-wrap
                  break-words
                  ${
                    msg.role === "user"
                      ? "bg-blue-600"
                      : "bg-slate-700"
                  }
                `}
              >

                <ReactMarkdown>
                  {msg.text}
                </ReactMarkdown>

              </div>

            </div>

          ))}



          {/* Loading */}

          {loading && (

            <div className="mb-6">

              <span className="
                text-sm
                text-slate-400
                block
                mb-1
              ">
                AI Assistant
              </span>

              <div className="
                bg-slate-700
                p-4
                rounded-2xl
                max-w-xl
              ">
                Thinking...
              </div>

            </div>

          )}



          {/* Auto Scroll */}

          <div ref={messagesEndRef}></div>

        </div>



        {/* Input Section */}

        <div className="
          flex
          gap-4
          mt-5
        ">

          <input
            className="
              flex-1
              p-4
              rounded-2xl
              bg-slate-700
              outline-none
            "
            placeholder="Ask something..."
            value={message}
            onChange={(e) =>
              setMessage(e.target.value)
            }
            onKeyDown={(e) => {

              if (e.key === "Enter") {
                sendMessage();
              }

            }}
          />



          <button
            className="
              bg-blue-600
              px-8
              rounded-2xl
              hover:bg-blue-500
              transition
              disabled:opacity-50
            "
            onClick={sendMessage}
            disabled={loading}
          >
            {
              loading
                ? "Sending..."
                : "Send"
            }
          </button>

        </div>

      </main>

    </div>
  );
}

export default Chat;