import streamlit as st
import pandas as pd
from fpdf import FPDF

# -------------------------------------------------
# PAGE CONFIG (Defined only once)
# -------------------------------------------------
st.set_page_config(page_title="Joint Point & Crossing Inspection", layout="wide")
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
        lh_opening = st.number_input("LH Opening", min_value=0.0, step=0.1, format="%.2f")
        lh_housing = st.number_input("LH Housing", min_value=0.0, step=0.1, format="%.2f")
        lh_joh = st.number_input(f"LH {label_name}", min_value=0.0, step=0.1, format="%.2f")
    with col_rh:
        st.markdown("### RH Side")
        rh_opening = st.number_input("RH Opening", min_value=0.0, step=0.1, format="%.2f")
        rh_housing = st.number_input("RH Housing", min_value=0.0, step=0.1, format="%.2f")
        rh_joh = st.number_input(f"RH {label_name}", min_value=0.0, step=0.1, format="%.2f")

    st.subheader("Gauge & Level")
    locations = ["150 MM", "5TH SLEEPER", "9TH SLEEPER"]
    gauge_level_data = {}
    for loc in locations:
        g1, g2 = st.columns(2)
        g = g1.text_input(f"Gauge at {loc}", placeholder="EXACT, -5, +3")
        l = g2.text_input(f"Level at {loc}", placeholder="7LL, 3RL")
        gauge_level_data[loc] = {"gauge": g, "level": l}

    remarks = st.text_area("Remarks")
    if st.form_submit_button("Save Record"):
        record = {
            "Point No": point_no, "Type": point_type,
            "LH Opening": lh_opening, "LH Housing": lh_housing, f"LH {label_name}": lh_joh,
            "RH Opening": rh_opening, "RH Housing": rh_housing, f"RH {label_name}": rh_joh,
            "Gauge_Level": gauge_level_data, "Remarks": remarks
        }
        st.session_state.data.append(record)
        st.success("Record Saved!")
        st.rerun()

# -------------------------------------------------
# VIEW & PDF CREATION
# -------------------------------------------------
st.header("Saved Records")
if not st.session_state.data:
    st.info("No records available")
else:
    for i, rec in enumerate(st.session_state.data):
        with st.expander(f"Point No: {rec['Point No']} | Type: {rec['Type']}"):
            st.write(f"LH Opening: {rec['LH Opening']} | RH Opening: {rec['RH Opening']}")
            if st.button(f"Delete Record {i+1}", key=f"del_{i}"):
                st.session_state.data.pop(i)
                st.rerun()

def create_pdf(records):
    pdf = FPDF()
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
        # Dynamic keys for JOH/Clearance
        lh_keys = [k for k in rec.keys() if "LH JOH" in k or "LH Clearance" in k]
        rh_keys = [k for k in rec.keys() if "RH JOH" in k or "RH Clearance" in k]
        lh_val = rec[lh_keys[0]] if lh_keys else "N/A"
        rh_val = rec[rh_keys[0]] if rh_keys else "N/A"
        locs = list(rec["Gauge_Level"].keys())
        
        # Helper to draw row
        def draw_row(side, opening, housing, j_val, loc_key):
            pdf.cell(18, 10, str(rec['Point No']), border=1)
            pdf.cell(10, 10, side, border=1, align="C")
            pdf.cell(18, 10, str(opening), border=1, align="C")
            pdf.cell(18, 10, str(housing), border=1, align="C")
            pdf.cell(20, 10, str(j_val), border=1, align="C")
            pdf.cell(25, 10, loc_key, border=1)
            pdf.cell(15, 10, str(rec['Gauge_Level'][loc_key]['gauge']), border=1, align="C")
            pdf.cell(25, 10, loc_key, border=1)
            pdf.cell(15, 10, str(rec['Gauge_Level'][loc_key]['level']), border=1, align="C")
            pdf.ln()

        draw_row("LH", rec['LH Opening'], rec['LH Housing'], lh_val, locs[0])
        draw_row("RH", rec['RH Opening'], rec['RH Housing'], rh_val, locs[1])
        # 3rd row for 3rd sleeper
        pdf.cell(84, 10, "", border=1)
        pdf.cell(25, 10, locs[2], border=1)
        pdf.cell(15, 10, str(rec['Gauge_Level'][locs[2]]['gauge']), border=1, align="C")
        pdf.cell(25, 10, locs[2], border=1)
        pdf.cell(15, 10, str(rec['Gauge_Level'][locs[2]]['level']), border=1, align="C")
        pdf.ln(10)
        
    return pdf.output(dest="S").encode("latin-1")

if st.session_state.data:
    st.download_button("Download PDF Report", data=create_pdf(st.session_state.data), file_name="report.pdf", mime="application/pdf")
