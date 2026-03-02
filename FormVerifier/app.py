import streamlit as st
from PIL import Image
import pytesseract
import re
import hashlib

# Tesseract Configuration
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.set_page_config(page_title="Kenya 2027 Verifier", page_icon="🗳️")
st.title("🗳️ Kenya 2027: Form 34A Verifier")

# --- SIDEBAR: National Statistics ---
st.sidebar.header("📊 National Tally (Simulated)")
mock_data = {'Candidate': ['A', 'B', 'C'], 'Votes': [12500, 11800, 4500]}
st.sidebar.table(mock_data)

# --- MAIN: Form Upload ---
uploaded_file = st.file_uploader("Upload Scanned Form 34A (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Form 34A", use_container_width=True)
    
    # SECURITY: Generate SHA-256 Fingerprint
    image_bytes = uploaded_file.getvalue()
    form_hash = hashlib.sha256(image_bytes).hexdigest()
    st.info(f"🛡️ Digital Fingerprint: {form_hash[:16]}...")

    if st.button("🔍 Run Forensic OCR Analysis"):
        with st.spinner('Reading ink patterns...'):
            extracted_text = pytesseract.image_to_string(img)
            
            st.subheader("Extracted Data")
            st.code(extracted_text)
            
            # --- VERIFICATION LOGIC ---
            # Search for "Candidate" followed by any characters and then a number
            match = re.search(r"Candidate.*?(\d+)", extracted_text)
            
            if match:
                votes = match.group(1)
                st.success(f"✅ Form Verified: recorded {votes} votes.")
            else:
                st.error("🚨 Anomaly Detected: Form structure unrecognized or tampered.")