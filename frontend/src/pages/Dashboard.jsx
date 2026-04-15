import { useState } from "react";
import Layout from "../components/common/Layout";

import UploadPage from "../features/upload/UploadPage";
import VerifyPage from "../features/verify/VerifyPage";
import IdentifyFingerprint from "../features/identity/IdentifyFingerprint";

export default function Dashboard() {
  const [tab, setTab] = useState("upload");

  return (
    <Layout>
      {/* Tabs */}
      <div className="tabs">
        <button
          className={tab === "upload" ? "active" : ""}
          onClick={() => setTab("upload")}
        >
          Upload
        </button>

        <button
          className={tab === "verify" ? "active" : ""}
          onClick={() => setTab("verify")}
        >
          Verify
        </button>

        <button
          className={tab === "identify" ? "active" : ""}
          onClick={() => setTab("identify")}
        >
          Identify
        </button>
      </div>

      {/* Content */}
      <div className="content">
        {tab === "upload" && <UploadPage />}
        {tab === "verify" && <VerifyPage />}
        {tab === "identify" && <IdentifyFingerprint />}
      </div>
    </Layout>
  );
}