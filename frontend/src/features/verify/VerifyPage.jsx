import { useState } from "react";
import { verifyFingerprint } from "../../services/api";

export default function VerifyPage() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [result, setResult] = useState(null);

  const handleVerify = async () => {
    if (!file1 || !file2) return;

    const res = await verifyFingerprint(file1, file2);
    setResult(res);
  };

  return (
    <div className="content">
      <h2>Verify Fingerprint</h2>

      <input type="file" onChange={(e) => setFile1(e.target.files[0])} />
      <br /><br />
      <input type="file" onChange={(e) => setFile2(e.target.files[0])} />

      <br /><br />

      <button onClick={handleVerify}>Verify</button>

      {result && (
        <div
          className="card"
          style={{
            border: result.match ? "2px solid green" : "2px solid red",
          }}
        >
          <h3>Result</h3>
          <p>Similarity: {result.similarity_score}</p>
          <p>
            Match:{" "}
            <strong style={{ color: result.match ? "green" : "red" }}>
              {result.match ? "YES" : "NO"}
            </strong>
          </p>
        </div>
      )}
    </div>
  );
}