import "./ApplyPage.css";
import { useState } from "react";
import axios from "axios";

function ApplyPage() {
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    position: "",
    resume: null,
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleFileChange = (e) => {
    setFormData({
      ...formData,
      resume: e.target.files[0],
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);

    const data = new FormData();

    data.append("name", formData.name);
    data.append("email", formData.email);
    data.append("phone", formData.phone);
    data.append("position", formData.position);
    data.append("file", formData.resume);

    try {
      await axios.post(
        "http://localhost:8000/upload-resume",
        data,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setSubmitted(true);
    } catch (error) {
      console.error("Upload Error:", error);
      alert("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="apply-container">

      <div className="company-name">
        Macenza Technology Private Limited
      </div>

      <div className="apply-card">

        <div className="header-section">
          <h1>Get Your Dream Job</h1>
          <p>
            Submit your application and let our ATS evaluate
            your profile for the best opportunities.
          </p>
        </div>

        {submitted ? (
          <div className="success-box">
            <div className="success-icon">✓</div>

            <h2>Application Submitted Successfully</h2>

            <p>
              Your application has been received.
              Our HR team will review your profile soon.
            </p>
          </div>
        ) : (
          <form
            onSubmit={handleSubmit}
            className="apply-form"
          >
            <input
              type="text"
              name="name"
              placeholder="Full Name"
              value={formData.name}
              onChange={handleChange}
              required
            />

            <input
              type="email"
              name="email"
              placeholder="Email Address"
              value={formData.email}
              onChange={handleChange}
              required
            />

            <input
              type="tel"
              name="phone"
              placeholder="Phone Number"
              value={formData.phone}
              onChange={handleChange}
              required
            />

            <input
              type="text"
              name="position"
              placeholder="Which job are you applying for?"
              value={formData.position}
              onChange={handleChange}
              required
            />

            <input
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={handleFileChange}
              required
            />

            <button
              type="submit"
              disabled={loading}
              className="submit-btn"
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Submitting...
                </>
              ) : (
                "Submit Application"
              )}
            </button>
          </form>
        )}

      </div>

    </div>
  );
}

export default ApplyPage;