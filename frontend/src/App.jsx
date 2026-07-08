import { BrowserRouter, Routes, Route } from "react-router-dom";

import Careers from "./pages/Careers";
import ApplyPage from "./pages/ApplyPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Career Page */}
        <Route path="/" element={<Careers />} />

        {/* Apply Form */}
        <Route path="/apply" element={<ApplyPage />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;