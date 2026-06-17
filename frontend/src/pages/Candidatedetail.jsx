import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

const CandidateDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCandidate();
  }, []);

  const fetchCandidate = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/applications`
      );

      const selectedCandidate = response.data.find(
        (item) => (item._id || item.id) === id
      );

      setCandidate(selectedCandidate);
    } catch (error) {
      console.error("Error fetching candidate", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <h2 style={{ padding: "30px" }}>Loading...</h2>;
  }

  if (!candidate) {
    return <h2 style={{ padding: "30px" }}>Candidate Not Found</h2>;
  }

  return (
    <div style={{ padding: "30px", background: "#f4f7fc", minHeight: "100vh" }}>
      <button
        onClick={() => navigate("/dashboard")}
        style={{
          padding: "10px 16px",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
          marginBottom: "20px",
        }}
      >
        Back to Dashboard
      </button>

      <div
        style={{
          background: "white",
          padding: "30px",
          borderRadius: "15px",
          boxShadow: "0 5px 20px rgba(0,0,0,0.08)",
        }}
      >
        <h1>{candidate.name}</h1>

        <hr style={{ margin: "20px 0" }} />

        <h3>Basic Information</h3>

        <p><strong>Email:</strong> {candidate.email}</p>
        <p><strong>Phone:</strong> {candidate.phone}</p>
        <p><strong>Position:</strong> {candidate.position}</p>
        <p><strong>Status:</strong> {candidate.status}</p>

        <hr style={{ margin: "20px 0" }} />

        <h3>ATS Score</h3>
        <p>
          <strong>
            {candidate.analysis?.ats_score || 0}
          </strong>
        </p>

        <hr style={{ margin: "20px 0" }} />

        <h3>AI Summary</h3>
        <p>{candidate.analysis?.summary || "No Summary Available"}</p>

        <hr style={{ margin: "20px 0" }} />

        <h3>Matched Skills</h3>
        <ul>
          {(candidate.analysis?.matched_skills || []).map((skill, index) => (
            <li key={index}>{skill}</li>
          ))}
        </ul>

        <hr style={{ margin: "20px 0" }} />

        <h3>Missing Skills</h3>
        <ul>
          {(candidate.analysis?.missing_skills || []).map((skill, index) => (
            <li key={index}>{skill}</li>
          ))}
        </ul>

        <hr style={{ margin: "20px 0" }} />

        <h3>Strengths</h3>
        <ul>
          {(candidate.analysis?.strengths || []).map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>

        <hr style={{ margin: "20px 0" }} />

        <h3>Weaknesses</h3>
        <ul>
          {(candidate.analysis?.weaknesses || []).map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>

        <hr style={{ margin: "20px 0" }} />

        <h3>Recommendations</h3>
        <ul>
          {(candidate.analysis?.recommendations || []).map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>

        <hr style={{ margin: "20px 0" }} />

        <h3>Interview Questions</h3>
        <ul>
          {(candidate.analysis?.top_interview_questions || []).map(
            (question, index) => (
              <li key={index}>{question}</li>
            )
          )}
        </ul>
      </div>
    </div>
  );
};

export default CandidateDetails;