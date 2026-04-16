# 🧬 DataDNA AI — File Ownership Fingerprinting System

## 🚀 Overview

DataDNA AI is an intelligent file ownership tracking system that embeds a unique, invisible fingerprint (DataDNA) into digital files. This fingerprint allows the system to identify the original owner—even if the file is modified, compressed, or leaked.

Unlike traditional watermarking, DataDNA AI focuses on **robust, AI-driven fingerprinting** that is difficult to remove and resilient to real-world transformations.

---

## 💡 Problem Statement

In today’s digital world, files are easily shared, copied, and leaked without accountability. Traditional solutions like visible watermarks or metadata tagging are:

* Easy to remove
* Not robust against edits
* Ineffective in proving ownership

---

## ✅ Solution

DataDNA AI embeds a **hidden, tamper-resistant fingerprint** into files and uses intelligent extraction techniques to recover ownership information later.

---

## ⚙️ How It Works

### 📤 Upload Phase

1. User uploads a file
2. System generates a unique fingerprint (DataDNA)
3. Fingerprint is embedded invisibly into the file
4. Watermarked file is stored securely

### 📥 Detection Phase

1. Suspicious file is uploaded
2. System extracts hidden fingerprint
3. Matches fingerprint with database
4. Returns original owner with confidence score

---

## 🧠 Role of AI

* Intelligent watermark embedding (autoencoder-based approach)
* Robust extraction even after:

  * Cropping
  * Compression
  * Noise addition
* Pattern reconstruction and matching

---

## 🏗️ System Architecture

```
User → Upload API → Fingerprint Generator → Watermark Engine → Storage
                                                   ↓
                                             Metadata Database

Leaked File → Detection API → Extraction Engine → Matching Engine → Result
```

---

## 🧩 Tech Stack

### Backend

* Python (FastAPI / Flask)

### AI / Processing

* OpenCV
* NumPy
* PyTorch / TensorFlow (for advanced models)

### Database

* MongoDB / PostgreSQL

### Frontend

* React (optional dashboard)

### Storage

* Google Cloud Storage (preferred) with local fallback

---

## 📁 Project Structure

```
datadna-ai/
│
├── backend/
├── frontend/
├── ai_models/
├── storage/
├── tests/
├── docs/
├── scripts/
│
├── README.md
├── requirements.txt
└── docker-compose.yml
```

---

## 🧪 Features

* 🔐 Invisible fingerprint embedding
* 🔍 Leak detection system
* 📊 Ownership verification with confidence score
* 🧠 AI-enhanced watermark robustness
* 📂 Support for scalable architecture

---

## 🚧 MVP Features (Current Version)

* Image upload system
* Basic watermark embedding (LSB)
* Watermark extraction
* Fingerprint matching

---

## 🔮 Future Enhancements

* AI-based watermarking (autoencoder)
* Video and PDF support
* Blockchain-based ownership logging
* Real-time leak monitoring
* SaaS dashboard for organizations

---

## ▶️ Getting Started

### 1. Clone Repository

```
git clone https://github.com/your-username/datadna-ai.git
cd datadna-ai
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Run Backend

```
cd backend/app
python main.py
```

### 4. Test API

* Upload: `POST /upload`
* Detect: `POST /detect`

### 5. Optional Google Cloud Storage Setup

Set these env vars to store files in Google Cloud Storage:

* `GCS_BUCKET_NAME`
* `GCP_PROJECT_ID` (optional if inferred by credentials)
* `GOOGLE_APPLICATION_CREDENTIALS` (path to service account json)

If `GCS_BUCKET_NAME` is not set, backend stores files on local disk.

---

## 📊 Example Response

```json
{
  "owner": "user123",
  "confidence": 0.94
}
```

---

## 🛡️ Security Considerations

* Fingerprints can be encrypted before embedding
* Resistant to basic tampering
* Future scope includes adversarial attack resistance

---

## 🤝 Contribution

Contributions are welcome. Feel free to fork the repo and submit pull requests.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## ⚡ Final Note

DataDNA AI is not just a watermarking tool—it is a **next-generation digital ownership verification system** designed for real-world leak detection and accountability.
