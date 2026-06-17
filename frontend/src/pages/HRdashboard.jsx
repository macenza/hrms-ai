import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./HRDashboard.css";

const HRDashboard = () => {
  const [applications, setApplications] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      const response = await axios.get("http://localhost:8000/applications");
      setApplications(response.data);
    } catch (error) {
      console.error("Error fetching applications", error);
    }
  };

  const updateStatus = async (id, status) => {
    try {
      await axios.put(`http://localhost:8000/applications/${id}`, {
        status,
      });

      fetchApplications();
    } catch (error) {
      console.error("Error updating status", error);
    }
  };

  // Search Filter
  const filteredApplications = applications.filter(
    (candidate) =>
      candidate.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      candidate.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      candidate.position?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Status Counts
  const pendingCount = applications.filter(
    (a) => a.status === "pending"
  ).length;

  const shortlistedCount = applications.filter(
    (a) => a.status === "shortlisted"
  ).length;

  const rejectedCount = applications.filter(
    (a) => a.status === "rejected"
  ).length;

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div>
          <h1>Macenza Technology Private Limited</h1>
          <p>Applicant Tracking System Dashboard</p>
        </div>
      </header>

      {/* STATS */}
      <div className="stats-container">
        <div className="stat-card">
          <h2>{applications.length}</h2>
          <p>Total Applications</p>
        </div>

        <div className="stat-card">
          <h2>{pendingCount}</h2>
          <p>Pending Review</p>
        </div>

        <div className="stat-card">
          <h2>{shortlistedCount}</h2>
          <p>Shortlisted</p>
        </div>

        <div className="stat-card">
          <h2>{rejectedCount}</h2>
          <p>Rejected</p>
        </div>
      </div>

      {/* SEARCH BAR */}
      <div className="search-container">
        <input
          type="text"
          placeholder="Search by Name, Email or Position..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {/* TABLE */}
      <div className="table-section">
        <h2>Candidate Applications</h2>

        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Position</th>
              <th>ATS Score</th>
              <th>Resume</th>
              <th>Status</th>
              <th>Action</th>
              <th>View</th>
            </tr>
          </thead>

          <tbody>
            {filteredApplications.map((candidate) => (
              <tr key={candidate._id || candidate.id}>
                <td>{candidate.name}</td>
                <td>{candidate.email}</td>
                <td>{candidate.phone}</td>
                <td>{candidate.position}</td>

                {/* ATS SCORE */}
                <td>
                  <strong>
                    {candidate.analysis?.ats_score || 0}
                  </strong>
                </td>

                {/* RESUME */}
                <td>{candidate.filename}</td>

                {/* STATUS */}
                <td>
                  <span className={`status ${candidate.status}`}>
                    {candidate.status}
                  </span>
                </td>

                {/* ACTION */}
                <td>
                  <select
                    value={candidate.status}
                    onChange={(e) =>
                      updateStatus(
                        candidate._id || candidate.id,
                        e.target.value
                      )
                    }
                    className="status-dropdown"
                  >
                    <option value="pending">Pending</option>
                    <option value="shortlisted">Shortlisted</option>
                    <option value="rejected">Rejected</option>
                  </select>
                </td>

                {/* VIEW BUTTON */}
                <td>
                  <button
                    className="view-btn"
                    onClick={() =>
                      navigate(
                        `/candidate/${candidate._id || candidate.id}`
                      )
                    }
                  >
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HRDashboard;