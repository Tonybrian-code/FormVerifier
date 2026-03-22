# 🗳️ Kenya 2027: Form 34A Forensic Verifier

### 📋 Project Overview
A specialized election integrity tool designed to bridge the "Trust Gap" in digital tallying. This application automates the verification of physical Form 34A images by cross-referencing AI-extracted data against a secure SQL "Source of Truth." 

Built as part of my **Year 3 Bachelor of IT** portfolio at **Multimedia University of Kenya (MMU)**.

### 🛡️ Forensic & Security Features
* **Integrity Hashing (SHA-256):** Every uploaded form generates a unique digital fingerprint. If a single pixel is altered, the hash changes, flagging the document as tampered.
* **Computer Vision (OCR):** Utilizes **Tesseract OCR** to convert "ink-on-paper" into machine-readable data. 
* **Noise-Resilient Logic:** Features a custom regex post-processing layer to handle common OCR "ghosting" (e.g., automatically sanitizing symbols like `&` to `Candidate A` or `8` to `Candidate B`).
* **Relational Audit Engine:** The system performs a real-time **SQLite3** lookup to ensure reported votes do not exceed the registered voter capacity of a specific polling station.
* **Stateful National Dashboard:** Implements **Streamlit Session State** to maintain a live-updating national tally that only accepts verified, legal votes.

### 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Frontend:** Streamlit (Reactive UI)
* **OCR Engine:** Tesseract OCR
* **Database:** SQLite3
* **Security:** Hashlib (SHA-256)

### 🚀 How to Run Locally
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/Tonybrian-code/FormVerifier.git](https://github.com/Tonybrian-code/FormVerifier.git)
   cd FormVerifier
   ```
2. **Setup Environment:**

python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt


3. **Initialize Database:**
   
python seed_db.py


4. **Launch App:** 
streamlit run app.py



---

### 🏛️ Engineering Reflection
The core challenge of this project was managing **"Dirty Data"** produced by the OCR engine. In real-world election scenarios, physical scans are rarely perfect. 

**Key Technical Solutions:**
* **Data Sanitization:** Implemented a mapping layer to correct OCR misidentifications (e.g., remapping symbols like `&` to `Candidate A` and `8` to `Candidate B`).
* **Tuple Unpacking:** Resolved critical `TypeError` bugs by manually unpacking SQLite result sets (e.g., `result`), ensuring the forensic audit could mathematically compare integers against database constants.

These refinements ensured the system's reliability remained intact even when faced with low-fidelity inputs, a crucial requirement for high-stakes forensic software.

---
© 2026 Tony | Year 3 BIT Student @ Multimedia University of Kenya
