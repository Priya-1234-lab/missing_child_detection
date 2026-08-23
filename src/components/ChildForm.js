import React, { useState } from "react";
import API from "../api";
import "./forms.css";


function ChildForm() {
  const [form, setForm] = useState({ name: "", dob: "", parent: "" });
  const [photo, setPhoto] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Create FormData object
    let data = new FormData();
    data.append("name", form.name);
    data.append("dob", form.dob);
    data.append("parent", form.parent);
    if (photo) data.append("photo", photo); // IMPORTANT

    try {
      const res = await API.post("/children/add/", data, {
        headers: { "Content-Type": "multipart/form-data" } // REQUIRED
      });
      alert("Child registered successfully!");
    } catch (err) {
      console.error(err.response.data); // See exact backend error
      alert("Registration failed! Check console for details.");
    }
  };

  return (
    <div className="form-container">
    <form onSubmit={handleSubmit}>
      <input
        name="name"
        placeholder="Child Name"
        onChange={(e) => setForm({ ...form, name: e.target.value })}
        required
      />
      <input
        type="date"
        name="dob"
        onChange={(e) => setForm({ ...form, dob: e.target.value })}
        required
      />
      <input
        name="parent"
        placeholder="Parent ID"
        onChange={(e) => setForm({ ...form, parent: e.target.value })}
        required
      />
      <input
        type="file"
        onChange={(e) => setPhoto(e.target.files[0])}
        required
      />
      <button type="submit">Register Child</button>
    </form>
    </div>
  );
}

export default ChildForm;