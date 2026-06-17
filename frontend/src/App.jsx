import { BrowserRouter, Routes, Route } from "react-router-dom";

import Careers from "./pages/Careers";
import ApplyPage from "./pages/ApplyPage";
import HRDashboard from "./pages/HRDashboard";
import CandidateDetails from "./pages/Candidatedetail"

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Career Page */}
        <Route path="/" element={<Careers />} />

        {/* Apply Form */}
        <Route path="/apply" element={<ApplyPage />} />

        {/* HR Dashboard */}
        <Route path="/dashboard" element={<HRDashboard />} />

        <Route path="/candidate/:id" element={<CandidateDetails />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;