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

      // Small Upload Notification
      setUploadStatus(
        `PDF "${file.name}" uploaded successfully`
      );

      // Auto Remove Notification
      setTimeout(() => {
        setUploadStatus("");
      }, 3000);

      // Clear File Input
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

    <div className="flex h-screen bg-slate-900 text-white">

      <Sidebar />

      <div className="flex-1 flex flex-col p-6">

        {/* Header */}

        <h1 className="text-4xl font-bold mb-6">
          AI Chat Assistant
        </h1>



        {/* Upload Section */}

        <div className="
          bg-slate-800
          p-4
          rounded-2xl
          shadow-lg
          mb-4
        ">

          <h2 className="text-lg font-semibold mb-3">
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
          p-4
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



              {/* Message Bubble */}

              <div
                className={`
                  p-4
                  rounded-2xl
                  max-w-2xl
                  whitespace-pre-wrap
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
                mb-1
                block
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



          {/* Auto Scroll Ref */}

          <div ref={messagesEndRef}></div>

        </div>



        {/* Input Section */}

        <div className="flex mt-4 gap-4">

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
              px-6
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

      </div>

    </div>
  );
}

export default Chat;