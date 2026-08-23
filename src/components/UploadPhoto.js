// frontend/src/components/UploadPhoto.js
import React, { useState } from "react";
import API from "../api";
import "./forms.css";


function getCurrentPositionAsync(options = { enableHighAccuracy: true, timeout: 10000 }) {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) return reject(new Error("Geolocation not supported"));
    navigator.geolocation.getCurrentPosition(resolve, reject, options);
  });
}

export default function UploadPhoto() {
  const [photo, setPhoto] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!photo) return alert("Please choose a photo.");

    // default values
    let locationText = "Unknown Location";
    let lat = "";
    let lon = "";

    // Try to get browser geolocation
    try {
      const pos = await getCurrentPositionAsync();
      lat = pos.coords.latitude;
      lon = pos.coords.longitude;

      // Optional: reverse geocode to human-readable address using Nominatim (OpenStreetMap)
      try {
        const r = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`);
        const j = await r.json();
        locationText = j.display_name || `Latitude: ${lat}, Longitude: ${lon}`;
      } catch (err) {
        // reverse geocode failed — use lat/lon fallback
        locationText = `Latitude: ${lat}, Longitude: ${lon}`;
      }
    } catch (err) {
      console.warn("Geolocation unavailable or denied:", err);
      locationText = "Unknown Location";
    }

    // Build form data
    const formData = new FormData();
    formData.append("photo", photo);
    formData.append("location", locationText);
    if (lat) formData.append("lat", lat);
    if (lon) formData.append("lon", lon);

    try {
      const res = await API.post("/children/search/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (res.data.match) {
        alert(`✅ Match found for ${res.data.child_name}!\nLocation used: ${res.data.location || locationText}`);
      } else {
        alert("No match found.");
      }
    } catch (error) {
      console.error("Search error:", error);
      if (error.response) {
        alert("Server error: " + JSON.stringify(error.response.data));
      } else {
        alert("Could not connect to server. Make sure backend is running.");
      }
    }
  };

  return (
    <div className="form-container">
    <form onSubmit={handleSearch}>
      <input type="file" accept="image/*" onChange={(e) => setPhoto(e.target.files[0])} required />
      <button type="submit">Search Child</button>
    </form>
    </div>
  );
}