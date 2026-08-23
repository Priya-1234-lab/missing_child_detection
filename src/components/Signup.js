import React, { useState } from "react";
import API from "../api";
import "./forms.css";


function Signup() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    phone: "",
    address: "",
    password: ""
  });

  const [parentId, setParentId] = useState(null); // ✅ to store parent ID

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await API.post("/accounts/signup/", form, {
        headers: { "Content-Type": "application/json" }
      });

      // ✅ Save parent ID from backend response
      setParentId(res.data.parent_id);

      alert(`✅ Signup Successful! Your Parent ID is: ${res.data.parent_id}`);
    } catch (err) {
      console.error("Signup error:", err.response?.data || err.message);
      alert("Signup Failed! Check console for details.");
    }
  };

  return (
    <div  className="form-container">
      
      <form onSubmit={handleSubmit}>
        <input name="username" placeholder="Username" onChange={handleChange} required />
        <input name="email" placeholder="Email" onChange={handleChange} required />
        <input name="phone" placeholder="Phone" onChange={handleChange} required />
        <input name="address" placeholder="Address" onChange={handleChange} required />
        <input name="password" type="password" placeholder="Password" onChange={handleChange} required />
        <button type="submit">Sign Up</button>
      </form>

      {/* ✅ Show parent ID if available */}
      {parentId && (
        <div style={{ marginTop: "20px", color: "green" }}>
          ✅ Your Parent ID is: <b>{parentId}</b>
          <br />
          (It has also been sent to your email)
        </div>
      )}
    </div>
  );
}

export default Signup;