import "./Careers.css";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

function Careers() {
  const navigate = useNavigate();

  const [searchTerm, setSearchTerm] = useState("");

  const jobs = [
    {
      title: "AI/ML Intern",
      location: "Remote",
      type: "Internship",
      description:
        "Work on Machine Learning, NLP and AI-powered applications.",
    },
    {
      title: "Frontend Developer",
      location: "Pune",
      type: "Full Time",
      description:
        "Build modern and responsive user interfaces using React.",
    },
    {
      title: "Backend Developer",
      location: "Remote",
      type: "Full Time",
      description:
        "Develop scalable APIs and backend systems using FastAPI.",
    },
    {
      title: "Data Analyst",
      location: "Remote",
      type: "Internship",
      description:
        "Analyze data and generate business insights.",
    },
    {
      title: "Python Developer",
      location: "Jaipur",
      type: "Full Time",
      description:
        "Build automation tools and backend applications.",
    },
    {
      title: "UI/UX Designer",
      location: "Remote",
      type: "Internship",
      description:
        "Design user-friendly interfaces and experiences.",
    },
    {
      title: "DevOps Engineer",
      location: "Remote",
      type: "Full Time",
      description:
        "Manage cloud infrastructure and deployment pipelines.",
    },
    {
  title: "Full Stack Developer",
  location: "Remote",
  type: "Full Time",
  description: "Build complete web applications."
},
{
  title: "Software Engineer",
  location: "Bangalore",
  type: "Full Time",
  description: "Develop scalable software solutions."
},
{
  title: "QA Engineer",
  location: "Remote",
  type: "Internship",
  description: "Test and ensure product quality."
}

  ];

  const filteredJobs = jobs.filter((job) =>
    job.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="careers-page">

      {/* Company Name */}
      <div className="company-name">
        Macenza Technology Private Limited
      </div>

      <header className="top-header">
        <div className="logo">
          HRMS <span>ATS Portal</span>
        </div>

        <p className="subtitle">
          Applicant Tracking & Recruitment System
        </p>
      </header>

      <section className="hero">
        <h1>Build Your Career With Us</h1>

        <p>
          Join our growing team and work on real-world AI,
          ML and Software Engineering projects.
        </p>

        <button
          className="hero-btn"
          onClick={() => navigate("/apply")}
        >
          View Open Positions
        </button>

        {/* Search Bar */}
        <div className="search-container">
          <input
            type="text"
            placeholder="Search jobs (AI, Frontend, Backend...)"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="job-search"
          />
        </div>
      </section>

      <section className="jobs-section">
        <h2>Open Positions</h2>

        <div className="jobs-grid">
          {filteredJobs.length > 0 ? (
            filteredJobs.map((job, index) => (
              <div className="job-card" key={index}>
                <h3>{job.title}</h3>

                <p>
                  <strong>Location:</strong> {job.location}
                </p>

                <p>
                  <strong>Type:</strong> {job.type}
                </p>

                <p>{job.description}</p>

                <button
                  className="details-btn"
                  onClick={() => navigate("/apply")}
                >
                  Apply Now
                </button>
              </div>
            ))
          ) : (
            <div className="no-jobs">
              No matching jobs found.
            </div>
          )}
        </div>
      </section>

      <section className="benefits">
        <h2>Why Join Us?</h2>

        <div className="benefit-grid">

          <div className="benefit-card">
            <h3>AI Powered Hiring</h3>
            <p>
              Smart ATS system that evaluates resumes automatically.
            </p>
          </div>

          <div className="benefit-card">
            <h3>Career Growth</h3>
            <p>
              Work on impactful engineering and AI projects.
            </p>
          </div>

          <div className="benefit-card">
            <h3>Remote Opportunities</h3>
            <p>
              Flexible work culture with remote opportunities.
            </p>
          </div>

          <div className="benefit-card">
            <h3>Modern Workspace</h3>
            <p>
              Fast, clean and structured recruitment platform.
            </p>
          </div>

        </div>
      </section>

    </div>
  );
}

export default Careers;