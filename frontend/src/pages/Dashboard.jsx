import { useEffect, useState } from "react";
import API from "../api/axios";

export default function Dashboard() {

  // =========================================
  // SHOW/HIDE AUTOMATION PANELS
  // =========================================

  const [showEmailAutomation, setShowEmailAutomation] =
    useState(false);

  const [showFollowupAutomation, setShowFollowupAutomation] =
    useState(false);

  // =========================================
  // EMAIL SUMMARY STATES
  // =========================================

  const [emailContent, setEmailContent] = useState("");
  const [emailResult, setEmailResult] = useState(null);
  const [emailLoading, setEmailLoading] = useState(false);

  // =========================================
  // FOLLOW-UP STATES
  // =========================================

  const [leadData, setLeadData] = useState({
    name: "",
    company: "",
    requirements: "",
  });

  const [followupResult, setFollowupResult] =
    useState(null);

  const [followupLoading, setFollowupLoading] =
    useState(false);

  // =========================================
  // CRM RECORDS
  // =========================================

  const [crmRecords, setCrmRecords] = useState([]);
  const [crmLoading, setCrmLoading] = useState(false);

  // =========================================
  // FETCH CRM RECORDS
  // =========================================

  const fetchCRMRecords = async () => {

    try {

      setCrmLoading(true);

      const response = await API.get(
        "/automation/crm/sync"
      );

      setCrmRecords(
        response.data.records || []
      );

    } catch (error) {

      console.error(
        "Failed to fetch CRM records:",
        error
      );

    } finally {

      setCrmLoading(false);
    }
  };

  // =========================================
  // LOAD CRM RECORDS
  // =========================================

  useEffect(() => {

    fetchCRMRecords();

  }, []);

  // =========================================
  // EMAIL AUTOMATION
  // =========================================

  const runEmailAutomation = async () => {

    if (!emailContent.trim()) {

      alert("Please paste email content.");

      return;
    }

    try {

      setEmailLoading(true);

      const response = await API.post(
        "/automation/email/summarize",
        {
          email_content: emailContent,
        }
      );

      console.log("EMAIL RESPONSE:");
      console.log(response.data);

      setEmailResult(response.data);

    } catch (error) {

      console.error(error);

      alert("Email automation failed.");

    } finally {

      setEmailLoading(false);
    }
  };

  // =========================================
  // FOLLOW-UP AUTOMATION
  // =========================================

  const runFollowupAutomation = async () => {

    try {

      setFollowupLoading(true);

      const response = await API.post(
  "/automation/followup/generate",
  {
    name: leadData.name,
    company: leadData.company,
    requirements: leadData.requirements,
    classification: "hot"
  }
);

      console.log("FOLLOWUP RESPONSE:");
      console.log(response.data);

      setFollowupResult(response.data);

      // Refresh CRM records
      fetchCRMRecords();

    } catch (error) {

      console.error(error);

      alert("Follow-up automation failed.");

    } finally {

      setFollowupLoading(false);
    }
  };

  return (

    <div className="
      min-h-screen
      bg-slate-950
      text-white
      p-8
    ">

      {/* ========================================= */}
      {/* PAGE TITLE */}
      {/* ========================================= */}

      <h1 className="
        text-4xl
        font-bold
        mb-10
      ">
        AI Business Assistant Dashboard
      </h1>

      {/* ========================================= */}
      {/* AUTOMATION CARDS */}
      {/* ========================================= */}

      <div className="
        grid
        grid-cols-1
        md:grid-cols-2
        gap-8
      ">

        {/* ========================================= */}
        {/* EMAIL SUMMARY CARD */}
        {/* ========================================= */}

        <div className="
          bg-slate-800
          rounded-2xl
          p-8
          shadow-xl
        ">

          <h2 className="
            text-3xl
            font-bold
            mb-4
          ">
            Email Summary Automation
          </h2>

          <p className="
            text-slate-300
            mb-6
          ">
            Generate AI summaries for emails.
          </p>

          <button
            onClick={() =>
              setShowEmailAutomation(
                !showEmailAutomation
              )
            }
            className="
              bg-blue-600
              hover:bg-blue-700
              px-6
              py-3
              rounded-xl
              font-semibold
            "
          >
            Run Automation
          </button>
        </div>

        {/* ========================================= */}
        {/* FOLLOW-UP CARD */}
        {/* ========================================= */}

        <div className="
          bg-slate-800
          rounded-2xl
          p-8
          shadow-xl
        ">

          <h2 className="
            text-3xl
            font-bold
            mb-4
          ">
            Follow-Up Automation
          </h2>

          <p className="
            text-slate-300
            mb-6
          ">
            Generate AI business follow-ups.
          </p>

          <button
            onClick={() =>
              setShowFollowupAutomation(
                !showFollowupAutomation
              )
            }
            className="
              bg-green-600
              hover:bg-green-700
              px-6
              py-3
              rounded-xl
              font-semibold
            "
          >
            Run Automation
          </button>
        </div>
      </div>

      {/* ========================================= */}
      {/* EMAIL AUTOMATION PANEL */}
      {/* ========================================= */}

      {showEmailAutomation && (

        <div className="
          mt-10
          bg-slate-800
          rounded-2xl
          p-8
          shadow-xl
        ">

          <h2 className="
            text-3xl
            font-bold
            mb-6
          ">
            Email Summary Automation
          </h2>

          <textarea
            rows={10}
            placeholder="Paste email content here..."
            value={emailContent}
            onChange={(e) =>
              setEmailContent(e.target.value)
            }
            className="
              w-full
              bg-slate-700
              rounded-xl
              p-4
              text-white
              outline-none
              mb-6
            "
          />

          <button
            onClick={runEmailAutomation}
            disabled={emailLoading}
            className="
              bg-blue-600
              hover:bg-blue-700
              px-6
              py-3
              rounded-xl
              font-semibold
            "
          >
            {emailLoading
              ? "Running..."
              : "Generate Summary"}
          </button>

          {/* RESULTS */}

          {emailResult && (

            <div className="
              mt-8
              bg-slate-700
              rounded-2xl
              p-6
              space-y-5
            ">

              <div>
                <h3 className="
                  text-xl
                  font-bold
                  mb-2
                ">
                  Summary
                </h3>

                <p>
                  {emailResult.summary ||
                    emailResult.result?.summary ||
                    emailResult.data?.summary}
                </p>
              </div>

              <div>
                <h3 className="
                  text-xl
                  font-bold
                  mb-2
                ">
                  Urgency
                </h3>

                <p>
                  {emailResult.urgency ||
                    emailResult.result?.urgency ||
                    emailResult.data?.urgency}
                </p>
              </div>

              <div>
                <h3 className="
                  text-xl
                  font-bold
                  mb-2
                ">
                  Action Items
                </h3>

                <ul className="
                  list-disc
                  ml-6
                ">
                  {(
                    emailResult.action_items ||
                    emailResult.result?.action_items ||
                    emailResult.data?.action_items ||
                    []
                  ).map(
                    (item, index) => (
                      <li key={index}>
                        {item}
                      </li>
                    )
                  )}
                </ul>
              </div>

              <div>
                <h3 className="
                  text-xl
                  font-bold
                  mb-2
                ">
                  Suggested Reply
                </h3>

                <div className="
                  bg-slate-800
                  p-4
                  rounded-xl
                  whitespace-pre-wrap
                ">
                  {emailResult.suggested_reply ||
                    emailResult.result?.suggested_reply ||
                    emailResult.data?.suggested_reply}
                </div>
              </div>

            </div>
          )}
        </div>
      )}

      {/* ========================================= */}
      {/* FOLLOW-UP AUTOMATION PANEL */}
      {/* ========================================= */}

      {showFollowupAutomation && (

        <div className="
          mt-10
          bg-slate-800
          rounded-2xl
          p-8
          shadow-xl
        ">

          <h2 className="
            text-3xl
            font-bold
            mb-6
          ">
            Follow-Up Automation
          </h2>

          <input
            type="text"
            placeholder="Client Name"
            value={leadData.name}
            onChange={(e) =>
              setLeadData({
                ...leadData,
                name: e.target.value,
              })
            }
            className="
              w-full
              bg-slate-700
              rounded-xl
              p-4
              text-white
              outline-none
              mb-4
            "
          />

          <input
            type="text"
            placeholder="Company"
            value={leadData.company}
            onChange={(e) =>
              setLeadData({
                ...leadData,
                company: e.target.value,
              })
            }
            className="
              w-full
              bg-slate-700
              rounded-xl
              p-4
              text-white
              outline-none
              mb-4
            "
          />

          <textarea
            rows={6}
            placeholder="Requirements"
            value={leadData.requirements}
            onChange={(e) =>
              setLeadData({
                ...leadData,
                requirements: e.target.value,
              })
            }
            className="
              w-full
              bg-slate-700
              rounded-xl
              p-4
              text-white
              outline-none
              mb-6
            "
          />

          <button
            onClick={runFollowupAutomation}
            disabled={followupLoading}
            className="
              bg-green-600
              hover:bg-green-700
              px-6
              py-3
              rounded-xl
              font-semibold
            "
          >
            {followupLoading
              ? "Generating..."
              : "Generate Follow-Up"}
          </button>

          {followupResult && (

            <div className="
              mt-8
              bg-slate-700
              rounded-2xl
              p-6
            ">

              <h3 className="
                text-2xl
                font-bold
                mb-4
              ">
                AI Follow-Up Email
              </h3>

              <div className="
                bg-slate-800
                p-5
                rounded-xl
                whitespace-pre-wrap
              ">

                {
  followupResult.data?.followup_email ||
  followupResult.followup?.followup_email ||
  followupResult.followup_email ||
  JSON.stringify(
    followupResult,
    null,
    2
  )
}

              </div>
            </div>
          )}
        </div>
      )}

      {/* ========================================= */}
      {/* CRM RECORDS */}
      {/* ========================================= */}

      <div className="
        mt-12
        bg-slate-800
        rounded-2xl
        p-8
        shadow-xl
      ">

        <h2 className="
          text-3xl
          font-bold
          mb-6
        ">
          CRM Records
        </h2>

        {crmLoading ? (

          <p>
            Loading CRM records...
          </p>

        ) : crmRecords.length === 0 ? (

          <p className="
            text-slate-400
          ">
            No CRM records found.
          </p>

        ) : (

          <div className="
            space-y-4
          ">

            {crmRecords.map(
              (record, index) => (

                <div
                  key={index}
                  className="
                    bg-slate-700
                    p-5
                    rounded-xl
                  "
                >

                  <p>
                    <strong>Name:</strong>
                    {" "}
                    {record.name}
                  </p>

                  <p>
                    <strong>Email:</strong>
                    {" "}
                    {record.email}
                  </p>

                  <p>
                    <strong>Company:</strong>
                    {" "}
                    {record.company}
                  </p>

                  <p>
                    <strong>Phone:</strong>
                    {" "}
                    {record.phone}
                  </p>

                  <p>
                    <strong>Requirements:</strong>
                    {" "}
                    {record.requirements}
                  </p>

                  <p>
                    <strong>Priority:</strong>
                    {" "}
                    {record.priority}
                  </p>

                  <p>
                    <strong>Timestamp:</strong>
                    {" "}
                    {record.timestamp}
                  </p>

                </div>
              )
            )}

          </div>
        )}
      </div>
    </div>
  );
}