import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Joint Point & Crossing Inspection",
    layout="wide"
)

st.title("Joint Point & Crossing Inspection System")

# -------------------------------------------------
# SESSION STORAGE
# -------------------------------------------------
if "data" not in st.session_state:
    st.session_state.data = []

# -------------------------------------------------
# ENTRY FORM
# -------------------------------------------------
st.header("Enter Inspection Details")

with st.form("inspection_form"):
    c1, c2 = st.columns(2)
    point_no = c1.text_input("Point No.")
    point_type = c2.radio("Type", ["TWS", "IRS"], horizontal=True)
    label_name = "JOH" if point_type == "TWS" else "Clearance"

    st.subheader("Measurement Details")
    col_lh, col_rh = st.columns(2)
    with col_lh:
        st.markdown("### LH Side")
        lh_opening = st.number_input("LH Opening", min_value=0, step=1, format="%d")
        lh_housing = st.number_input("LH Housing", min_value=0, step=1, format="%d")
        lh_joh = st.number_input(f"LH {label_name}", min_value=0, step=1, format="%d")
    with col_rh:
        st.markdown("### RH Side")
        rh_opening = st.number_input("RH Opening", min_value=0, step=1, format="%d")
        rh_housing = st.number_input("RH Housing", min_value=0, step=1, format="%d")
        rh_joh = st.number_input(f"RH {label_name}", min_value=0, step=1, format="%d")

    st.subheader("Gauge & Level")
    locations = ["150 MM", "5TH SLEEPER", "9TH SLEEPER"]
    gauge_level_data = {}
    for loc in locations:
        c1, c2 = st.columns(2)
        g = c1.text_input(f"Gauge at {loc}", placeholder="Example: EXACT, -5, +3")
        le = c2.text_input(f"Level at {loc}", placeholder="Example: 7LL, 3RL")
        gauge_level_data[loc] = {"gauge": g, "level": le}

    remarks = st.text_area("Remarks")
    if st.form_submit_button("Save Record"):
        record = {
            "Point No": point_no, "Type": point_type,
            "LH Opening": lh_opening, "LH Housing": lh_housing, f"LH {label_name}": lh_joh,
            "RH Opening": rh_opening, "RH Housing": rh_housing, f"RH {label_name}": rh_joh,
            "Gauge_Level": gauge_level_data, "Remarks": remarks
        }
        st.session_state.data.append(record)
        st.success("Record Saved Successfully")

# -------------------------------------------------
# PDF CREATION
# -------------------------------------------------
def create_pdf(records):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, "JOINT POINT & CROSSING INSPECTION", border=1, ln=True, align="C")
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 8)
    headers = ["PT NO.", "SIDE", "OPENING", "HOUSING", "CLR/JOH", "GAUGE LOC", "GAUGE", "LEVEL LOC", "LEVEL"]
    widths = [18, 10, 18, 18, 20, 25, 15, 25, 15]
    for h, w in zip(headers, widths):
        pdf.cell(w, 10, h, border=1, align="C")
    pdf.ln()

    pdf.set_font("Arial", "", 8)
    for rec in records:
        lh_key = [k for k in rec.keys() if "LH JOH" in k or "LH Clearance" in k][0]
        rh_key = [k for k in rec.keys() if "RH JOH" in k or "RH Clearance" in k][0]
        locs = list(rec["Gauge_Level"].keys())
        
        # LH Row
        pdf.cell(18, 10, str(rec['Point No']), border=1)
        pdf.cell(10, 10, "LH", border=1, align="C")
        pdf.cell(18, 10, str(rec['LH Opening']), border=1, align="C")
        pdf.cell(18, 10, str(rec['LH Housing']), border=1, align="C")
        pdf.cell(20, 10, str(rec[lh_key]), border=1, align="C")
        pdf.cell(25, 10, locs[0], border=1)
        pdf.cell(15, 10, str(rec['Gauge_Level'][locs[0]]['gauge']), border=1, align="C")
        pdf.cell(25, 10, locs[0], border=1)
        pdf.cell(15, 10, str(rec['Gauge_Level'][locs[0]]['level']), border=1, align="C")
        pdf.ln()
        
        # RH Row
        pdf.cell(18, 10, "", border=1)
        pdf.cell(10, 10, "RH", border=1, align="C")
        pdf.cell(18, 10, str(rec['RH Opening']), border=1, align="C")
        pdf.cell(18, 10, str(rec['RH Housing']), border=1, align="C")
        pdf.cell(20, 10, str(rec[rh_key]), border=1, align="C")
        pdf.cell(25, 10, locs[1], border=1)
        pdf.cell(15, 10, str(rec['Gauge_Level'][locs[1]]['gauge']), border=1, align="C")
        pdf.cell(25, 10, locs[1], border=1)
        pdf.cell(15, 10, str(rec['Gauge_Level'][locs[1]]['level']), border=1, align="C")
        pdf.ln()
        
        # 3rd Sleeper row
        pdf.cell(18, 10, "", border=1)
        pdf.cell(10, 10, "", border=1)
        pdf.cell(18, 10, "", border=1)
        pdf.cell(18, 10, "", border=1)
        pdf.cell(20, 10, "", border=1)
        pdf.cell(25, 10, locs[2], border=1)
        pdf.cell(15, 10, str(rec['Gauge_Level'][locs[2]]['gauge']), border=1, align="C")
        pdf.cell(25, 10, locs[2], border=1)
        pdf.cell(15, 10, str(rec['Gauge_Level'][locs[2]]['level']), border=1, align="C")
        pdf.ln(10)
    return pdf.output(dest="S").encode("latin-1")

if st.session_state.data:
    st.download_button("Download PDF Report", data=create_pdf(st.session_state.data), file_name="report.pdf", mime="application/pdf")
