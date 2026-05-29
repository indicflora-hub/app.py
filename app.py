import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")
st.title("Joint Point & Crossing Inspection")

# 1. Initialize Session State
if 'data' not in st.session_state:
    # Based on your requested format:
    # PT NO | TYPE | SIDE | OPENING | HOUSING | JOH/CLR | LOC | GAUGE | LEVEL | REMARKS
    st.session_state.data = pd.DataFrame(columns=[
        "PT NO.", "TYPE", "SIDE", "OPENING", "HOUSING", "JOH/CLR", "LOC", "GAUGE", "LEVEL", "REMARKS"
    ])

# 2. Entry Form
st.header("Inspection Entry")
with st.form(key="inspection_form_main"):
    col_a, col_b = st.columns(2)
    with col_a:
        pt_no = st.text_input("Point No.")
    with col_b:
        point_type = st.radio("Point Type", ["TWS", "IRS"], horizontal=True)
    
    jc_label = "JOH" if point_type == "TWS" else "Clearance"
    
    # Side-specific inputs
    st.subheader("General Point Data (Per Side)")
    c1, c2 = st.columns(2)
    with c1:
        st.write("### LH Side")
        lh_op = st.number_input("LH Opening", step=1)
        lh_ho = st.number_input("LH Housing", step=1)
        lh_jc = st.number_input(f"LH {jc_label}", step=1)
    with c2:
        st.write("### RH Side")
        rh_op = st.number_input("RH Opening", step=1)
        rh_ho = st.number_input("RH Housing", step=1)
        rh_jc = st.number_input(f"RH {jc_label}", step=1)

    # Location-based inputs (Not side-specific, Alphanumeric allowed)
    st.subheader("Gauge & Level Measurements (Per Location)")
    locs = ["150 mm", "5th Sleeper", "9th Sleeper"]
    loc_data = {}
    
    for loc in locs:
        st.write(f"**{loc}**")
        g1, l1 = st.columns(2)
        loc_data[(loc, "G")] = g1.text_input(f"Gauge ({loc})", key=f"g_{loc}", placeholder="e.g. +2mm")
        loc_data[(loc, "L")] = l1.text_input(f"Level ({loc})", key=f"l_{loc}", placeholder="e.g. -1mm")

    remarks = st.text_area("Remarks")
    submitted = st.form_submit_button("Save Inspection")

# 3. Data Processing
if submitted and pt_no:
    rows = []
    # LH Side Row
    rows.append({
        "PT NO.": pt_no, "TYPE": point_type, "SIDE": "LH", "OPENING": lh_op, "HOUSING": lh_ho, 
        "JOH/CLR": lh_jc, "LOC": "N/A", "GAUGE": "N/A", "LEVEL": "N/A", "REMARKS": remarks
    })
    # RH Side Row
    rows.append({
        "PT NO.": pt_no, "TYPE": point_type, "SIDE": "RH", "OPENING": rh_op, "HOUSING": rh_ho, 
        "JOH/CLR": rh_jc, "LOC": "N/A", "GAUGE": "N/A", "LEVEL": "N/A", "REMARKS": remarks
    })
    # Location rows (Gauge/Level only)
    for loc in locs:
        rows.append({
            "PT NO.": pt_no, "TYPE": point_type, "SIDE": "N/A", "OPENING": "N/A", "HOUSING": "N/A", 
            "JOH/CLR": "N/A", "LOC": loc, "GAUGE": loc_data[(loc, "G")], 
            "LEVEL": loc_data[(loc, "L")], "REMARKS": remarks
        })
        
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame(rows)], ignore_index=True)
    st.success(f"Point {pt_no} saved!")
    st.rerun()

# 4. Summary & Export
st.subheader("Inspection Summary")
st.data_editor(st.session_state.data, num_rows="dynamic")

# Excel Export
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

st.download_button("Download Excel", data=to_excel(st.session_state.data), file_name="Inspection_Log.xlsx")
