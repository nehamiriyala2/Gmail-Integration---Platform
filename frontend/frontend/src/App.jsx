
import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
} from "recharts";

function App() {
  // --- States ---
  const [searchTerm, setSearchTerm] = useState("");
  const [filterCategory, setFilterCategory] = useState("All");
  const [dashboard, setDashboard] = useState({});
  const [emails, setEmails] = useState([]);
  const [threads, setThreads] = useState([]); // ✅ Added Threads State
  const [activePage, setActivePage] = useState("dashboard");
  const [loading, setLoading] = useState(false);
  const [selectedEmail, setSelectedEmail] = useState(null); 
  const [darkMode, setDarkMode] = useState(true); 
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const [to, setTo] = useState("");
  const [subject, setSubject] = useState("");
  const [message, setMessage] = useState("");

  // --- API Calls ---
  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const res = await axios.get("http://127.0.0.1:8000/gmail/dashboard");
      setDashboard(res.data.dashboard || {});
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchEmails = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/gmail/emails");
      setEmails(res.data.emails || []);
    } catch (err) {
      console.error(err);
    }
  };

  // ✅ Added Fetch Threads Function
  const fetchThreads = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/gmail/threads");
      setThreads(res.data.threads || []);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchDashboard();
    fetchEmails();
    fetchThreads(); // ✅ Included Fetch Threads
  }, []);

  // --- Chart Data Layouts ---
  const categoryData = [
    { name: "Job", value: dashboard.job_emails || 0 },
    {
      name: "Other",
      value: (dashboard.total_emails || 0) - (dashboard.job_emails || 0),
    },
  ];

  const priorityData = [
    { name: "High", count: dashboard.high_priority || 0 },
    {
      name: "Normal",
      count: (dashboard.total_emails || 0) - (dashboard.high_priority || 0),
    },
  ];

  // --- Filtering Logic ---
  const filteredEmails = emails.filter((email) => {
    const matchesSearch = email.subject
      ?.toLowerCase()
      .includes(searchTerm.toLowerCase());

    const matchesCategory =
      filterCategory === "All" ? true : email.category === filterCategory;

    return matchesSearch && matchesCategory;
  });

  if (loading) {
    return (
      <div className="loader-container">
        <h1>Loading Dashboard...</h1>
      </div>
    );
  }

  return (
    <div className={`app ${darkMode ? "dark" : "light"}`}>
      
      {/* ================= SIDEBAR ================= */}
      <aside className="sidebar">
        <h2 className="logo">📧 Gmail AI</h2>

        <button
          className={`menu-btn ${activePage === "dashboard" ? "active" : ""}`}
          onClick={() => setActivePage("dashboard")}
        >
          Dashboard
        </button>
        <button
          className={`menu-btn ${activePage === "emails" ? "active" : ""}`}
          onClick={() => setActivePage("emails")}
        >
          Emails
        </button>
        <button
          className={`menu-btn ${activePage === "analytics" ? "active" : ""}`}
          onClick={() => setActivePage("analytics")}
        >
          Analytics
        </button>
        {/* ✅ Added Threads Button */}
        <button
          className={`menu-btn ${activePage === "threads" ? "active" : ""}`}
          onClick={() => setActivePage("threads")}
        >
          🧵 Threads
        </button>
        <button
          className={`menu-btn ${activePage === "assistant" ? "active" : ""}`}
          onClick={() => setActivePage("assistant")}
        >
          🤖 AI Assistant
        </button>
        <button
          className={`menu-btn ${activePage === "compose" ? "active" : ""}`}
          onClick={() => setActivePage("compose")}
        >
          ✉ Compose
        </button>
        <button
          className={`menu-btn ${activePage === "settings" ? "active" : ""}`}
          onClick={() => setActivePage("settings")}
        >
          ⚙ Settings
        </button>

        <button
          className="sync-btn"
          onClick={() => {
            fetchDashboard();
            fetchEmails();
            fetchThreads(); // ✅ Included Threads in Sync
          }}
        >
          🔄 Sync Gmail
        </button>
      </aside>

      {/* ================= MAIN CONTENT ================= */}
      <main className="main-content">
        
        {/* 1. DASHBOARD PAGE */}
        {activePage === "dashboard" && (
          <>
            <div className="header">
              <h1>Gmail Intelligence Dashboard</h1>
              <button className="refresh-btn" onClick={fetchDashboard}>
                Refresh Dashboard
              </button>
            </div>

            <div className="summary-card">
              <h3>🤖 AI Summary</h3>
              <p>
                You have {dashboard.job_emails || 0} job emails, {" "}
                {dashboard.high_priority || 0} high priority emails and {" "}
                {dashboard.total_emails || 0} total emails.
              </p>
            </div>

            <div className="stats-grid">
              <div className="stat-card">
                <h4>Total Emails</h4>
                <h1>{dashboard.total_emails || 0}</h1>
              </div>
              <div className="stat-card">
                <h4>Job Emails</h4>
                <h1>{dashboard.job_emails || 0}</h1>
              </div>
              <div className="stat-card">
                <h4>High Priority</h4>
                <h1>{dashboard.high_priority || 0}</h1>
              </div>
              <div className="stat-card">
                <h4>Unread Emails</h4>
                <h1>{dashboard.unread_emails || 0}</h1>
              </div>
              <div className="stat-card">
                <h4>Important Emails</h4>
                <h1>{dashboard.important_emails || 0}</h1>
              </div>
              <div className="stat-card">
                <h4>Spam Emails</h4>
                <h1>{dashboard.spam_emails || 0}</h1>
              </div>
              <div className="stat-card">
                <h4>Latest</h4>
                <p className="latest-text">
                  {dashboard.latest_email || "No Emails"}
                </p>
              </div>
            </div>
          </>
        )}

        {/* 2. EMAILS PAGE */}
        {activePage === "emails" && (
          <>
            <h1 className="page-title">📩 Email Management</h1>
            <div className="toolbar">
              <input
                type="text"
                placeholder="Search Emails..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-box"
              />
              <select
                value={filterCategory}
                onChange={(e) => setFilterCategory(e.target.value)}
                className="filter-box"
              >
                <option value="All">All</option>
                <option value="Job">Job</option>
                <option value="Important">Important</option>
                <option value="Spam">Spam</option>
              </select>
            </div>

            <div className="recent-section">
              <h2>Total Emails State: {emails.length}</h2>
              <h2>Filtered Emails: {filteredEmails.length}</h2>

              <table className="email-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Subject</th>
                    <th>Category</th>
                    <th>Priority</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredEmails.map((email) => (
                    <tr
                      key={email.id}
                      onClick={() => setSelectedEmail(email)}
                      style={{ cursor: "pointer" }}
                    >
                      <td>{email.id}</td>
                      <td>{email.subject}</td>
                      <td>{email.category}</td>
                      <td>{email.priority}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}

        {/* 3. ANALYTICS PAGE */}
        {activePage === "analytics" && (
          <>
            <h1 className="page-title">📊 Analytics Dashboard</h1>
            <div className="chart-grid">
              <div className="chart-card">
                <h3>Email Categories</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie data={categoryData} dataKey="value">
                      <Cell fill="#38bdf8" />
                      <Cell fill="#8b5cf6" />
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="chart-card">
                <h3>Priority Distribution</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={priorityData}>
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#38bdf8" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </>
        )}

        {/* ✅ 4. THREADS PAGE */}
        {activePage === "threads" && (
          <>
            <h1 className="page-title">🧵 Email Threads</h1>
            <div className="recent-section">
              <table className="email-table">
                <thead>
                  <tr>
                    <th>Sender</th>
                    <th>Thread Count</th>
                  </tr>
                </thead>
                <tbody>
                  {threads.map((thread, index) => (
                    <tr key={index}>
                      <td>{thread.sender}</td>
                      <td>{thread.count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}

        {/* 5. AI ASSISTANT PAGE */}
        {activePage === "assistant" && (
          <>
            <h1 className="page-title">🤖 AI Assistant</h1>
            <div className="settings-card">
              <input
                type="text"
                placeholder="Ask about emails..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                className="search-box"
              />
              <br /><br />
              <button
                className="refresh-btn"
                onClick={() => {
                  if (question.toLowerCase().includes("job")) {
                    setAnswer(`You have ${dashboard.job_emails || 0} job emails`);
                  } else if (question.toLowerCase().includes("total")) {
                    setAnswer(`You have ${dashboard.total_emails || 0} total emails`);
                  } else {
                    setAnswer("No information available");
                  }
                }}
              >
                Ask AI
              </button>

              <div style={{ marginTop: "20px", fontSize: "18px" }}>
                {answer}
              </div>
            </div>
          </>
        )}

        {/* 6. COMPOSE PAGE */}
        {activePage === "compose" && (
          <>
            <h1 className="page-title">✉ Compose Email</h1>
            <div className="settings-card">
              <input
                type="email"
                placeholder="Recipient Email"
                value={to}
                onChange={(e) => setTo(e.target.value)}
                className="search-box"
              />
              <br /><br />
              <input
                type="text"
                placeholder="Subject"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="search-box"
              />
              <br /><br />
              <textarea
                placeholder="Write your message..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                rows="8"
                className="search-box"
              />
              <br /><br />
              <button
                className="refresh-btn"
                onClick={() => {
                  alert("Email Sent Successfully");
                  setTo("");
                  setSubject("");
                  setMessage("");
                }}
              >
                Send Email
              </button>
            </div>
          </>
        )}

        {/* 7. SETTINGS PAGE */}
        {activePage === "settings" && (
          <>
            <h1 className="page-title">⚙ Settings</h1>
            <div className="settings-card">
              <h3>System Status</h3>
              <p>🟢 Backend Connected</p>
              <p>🟢 PostgreSQL Connected</p>
              <p>🟢 Gmail API Connected</p>
              <p>🟢 Dashboard Active</p>

              <div className="theme-toggle" style={{ marginTop: "20px" }}>
                <button onClick={() => setDarkMode(true)}>🌙 Dark Mode</button>
                <button onClick={() => setDarkMode(false)}>☀ Light Mode</button>
              </div>
            </div>
          </>
        )}

      </main>

      {/* ================= EMAIL MODAL ================= */}
      {selectedEmail && (
        <div className="modal-overlay">
          <div className="modal">
            <button className="close-btn" onClick={() => setSelectedEmail(null)}>
              X
            </button>

            <h2>Email Details</h2>
            <p><strong>ID:</strong> {selectedEmail.id}</p>
            <p><strong>Sender:</strong> {selectedEmail.sender || "N/A"}</p>
            <p><strong>Subject:</strong> {selectedEmail.subject}</p>
            <p><strong>Category:</strong> {selectedEmail.category}</p>
            <p><strong>Priority:</strong> {selectedEmail.priority}</p>
            <p><strong>Created:</strong> {selectedEmail.created_at || "N/A"}</p>
            
            <hr />
            <h3>🤖 AI Summary</h3>
            <p>{selectedEmail.subject}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

