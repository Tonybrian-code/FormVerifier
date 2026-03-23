import streamlit as st
from PIL import Image
import pytesseract
import re
import hashlib
import sqlite3
import os


# Create a 'Session State' to store the national tally
if 'tally_results' not in st.session_state:
    st.session_state.tally_results = {'A': 12500, 'B': 11800, 'C': 4500}

# Tesseract Configuration
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.set_page_config(page_title="Kenya 2027 Verifier", page_icon="🗳️")
st.title("🗳️ Kenya 2027: Form 34A Verifier")

# National Statistics
st.sidebar.header("📊 National Tally (Simulated)")
mock_data = {'Candidate': ['A', 'B', 'C'], 'Votes': [12500, 11800, 4500]}
st.sidebar.table(st.session_state.tally_results)

# Form Upload
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
            
            # CONSOLIDATED FORENSIC EXTRACTION
            # Regex code to find the Candidate identifier and the Vote count
            match = re.search(r"Candidate.*?(\w|&).*?(\d+)", extracted_text)

            if match:
                raw_candidate = match.group(1) 
                votes = int(match.group(2)) # Successfully converts the digits to an integer
                
                # DATA SANITIZATION
                # Mapping messy OCR characters back to the correct database keys
                if raw_candidate in ['A', '&']: 
                    candidate_key = 'A'
                elif raw_candidate in ['B', '8']: 
                    candidate_key = 'B'
                else: 
                    candidate_key = 'C'
        
                st.success(f"✅ OCR identified {candidate_key} with {votes} votes.")

                # Catches PS-002, P-002, or even P 002
                id_match = re.search(r"P[S]?[- ]?(\d+)", extracted_text)
                station_id = f"PS-{id_match.group(1)}" if id_match else "PS-001"

                # DATABASE AUDIT
                current_dir = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.join(current_dir, 'constituency_data.db')

                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute("SELECT expected_voters FROM polling_stations WHERE id=?", (station_id,))
                result = c.fetchone()
                conn.close()

                if result:
                    expected_capacity = result[0] #so the number cannot be in a tuple
                    st.info(f"📋 Database Check: Station {station_id} has a max capacity of {expected_capacity} voters.")
                    
                    # THE VERDICT
                    if votes > expected_capacity:
                        st.error(f"🚨 DISCREPANCY: Votes ({votes}) exceed capacity!")
                    else:
                        st.success(f"⚖️ Mathematical Validation: {station_id} result is legal.")
                        
                        # THE LIVE UPDATE
                        # Correctly updates the specific candidate found by the sanitized logic
                        st.session_state.tally_results[candidate_key] += votes
                        
                        st.balloons() 
                        st.info(f"🗳️ National Tally updated for Candidate {candidate_key}!")
                        
                        st.rerun()