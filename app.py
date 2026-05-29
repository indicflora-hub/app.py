import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

st.set_page_config(layout="wide")
st.title("Joint Point & Crossing Inspection")

if 'data' not in st.session_state:
    st.session_state.data = []

with st.form("entry_form"):
    c1, c2 = st.columns(2)
    pt = c1.text_input("Point No.")
    typ = c2.radio("Type", ["TWS", "IRS"], horizontal=True)
    
    label = "JOH" if typ == "TWS" else "Clearance"
    
    col_lh, col_rh = st.columns(2)
    lh = {"op": col_lh.number_input("LH Op"), "ho": col_lh.number_input("LH Ho"), "jc": col_lh.number_input(f"LH {label}")}
    rh = {"op": col_rh.number_input("RH Op"), "ho": col_rh.number_input("RH Ho"), "jc": col_rh.number_input(f"RH {label}")}
    
    locs = ["150 MM", "5TH SLEEPER", "9TH SLEEPER"]
    loc_data = {}
    for l in locs:
        g, le = st.columns(2)
        loc_data[l] = {"g": g.text_input(f"Gauge {l}"), "le": le.text_input(f"Level {l}")}
    
    rem = st.text_area("Remarks")
    if st.form_submit_button("Save"):
        st.session_state.data.append({"pt": pt, "type": typ, "lh": lh, "rh": rh, "locs": loc_data, "rem": rem})
        st.rerun()

st.subheader("Records")
for i, entry in enumerate(st.session_state.data):
    st.write(f"Point: {entry['pt']} | Type: {entry['type']}")
    if st.button(f"Delete Record {i+1}"):
        st.session_state.data.pop(i)
        st.rerun()

# PDF Generator
def make_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    for entry in data:
        pdf.cell(200, 10, txt=f"Point: {entry['pt']} ({entry['type']})", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.cell(200, 7, txt=f"LH Opening: {entry['lh']['op']} | RH Opening: {entry['rh']['op']}", ln=True)
        pdf.cell(200, 7, txt=f"Remarks: {entry['rem']}", ln=True)
        pdf.ln(5)
    return pdf.output(dest='S').encode('latin-1')

if st.session_state.data:
    st.download_button("Download PDF", data=make_pdf(st.session_state.data), file_name="report.pdf", mime="application/pdf")
