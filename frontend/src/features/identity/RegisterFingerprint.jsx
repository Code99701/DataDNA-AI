console.log("REGISTER COMPONENT ACTIVE");
import { useState } from "react";
import { registerIdentity } from "../../services/api";

export default function RegisterFingerprint() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    userId: "",
    organisation: "",
  });

  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRegister = async () => {
    if (!file) {
      alert("Please upload a fingerprint image");
      return;
    }

    try {
      setLoading(true);

      const res = await registerIdentity(file); // 🔥 API CALL

      console.log("Response:", res);
      setResult(res);
    } catch (err) {
      console.error("Error:", err);
      alert("Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <h2>Register Your Identity</h2>

      {/* Form Fields */}
      <input
        type="text"
        name="name"
        placeholder="Full Name"
        value={form.name}
        onChange={handleChange}
      />

      <input
        type="email"
        name="email"
        placeholder="Email"
        value={form.email}
        onChange={handleChange}
      />

      <input
        type="text"
        name="userId"
        placeholder="User ID"
        value={form.userId}
        onChange={handleChange}
      />

      <input
        type="text"
        name="organisation"
        placeholder="Organisation (optional)"
        value={form.organisation}
        onChange={handleChange}
      />

      {/* File Upload */}
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      {/* Button */}
      <button onClick={handleRegister} disabled={loading}>
        {loading ? "Registering..." : "Create Digital Identity"}
      </button>

      {/* Result */}
      {result && result.fingerprint_id && (
  <div style={{ marginTop: "20px", color: "white" }}>
    <p><strong>Fingerprint Generated ✅</strong></p>

    <p><b>ID:</b> {result.fingerprint_id.fingerprint}</p>

    <p><b>Hash:</b> {result.fingerprint_id.hash}</p>

    {/* Optional */}
    {/* <p>{result.fingerprint_id.binary}</p> */}
  </div>
)}
    </div>
  );
}