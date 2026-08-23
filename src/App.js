import React from "react";
import "./App.css";
import Signup from "./components/Signup";
import ChildForm from "./components/ChildForm";
import UploadPhoto from "./components/UploadPhoto";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

function App() {
  return (
    <Router>
      <div className="dashboard-container">
        <h1 className="dashboard-title">Detecto!🔍</h1>

        <div className="card-wrapper">
          <div className="glass-card">
            <h2>Sign Up</h2>
            <p>Create parent account</p>
            <Link to="/signup" className="glass-btn">Open</Link>
          </div>

          <div className="glass-card">
            <h2>Register Child</h2>
            <p>Add missing child details</p>
            <Link to="/register" className="glass-btn">Open</Link>
          </div>

          <div className="glass-card">
            <h2>Search Child</h2>
            <p>Find child in records</p>
            <Link to="/search" className="glass-btn">Start</Link>
          </div>
        </div>

        <Routes>
          <Route path="/signup" element={<Signup />} />
          <Route path="/register" element={<ChildForm />} />
          <Route path="/search" element={<UploadPhoto />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
