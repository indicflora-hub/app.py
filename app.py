import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")
st.title("Joint Point & Crossing Inspection")

# 1. Initialize Session State
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "PT NO.", "TYPE", "SIDE", "LOC", 
        "OPENING", "HOUSING", "JOH/CLR", "GAUGE", "LEVEL", "REMARKS"
    ])

# 2. Entry Form
st.header("Inspection Entry")
with st.form(key="inspection_form_main"):
    col_a, col_b = st.columns(2)
    with col_a:
        pt_no = st.text_input("Point No.")
    with col_b:
        point_type = st.radio("Point Type", ["TWS", "IRS"], horizontal=True)
    
    # JOH or Clearance label based on type
    jc_label = "JOH" if point_type == "TWS" else "Clearance"
    
    # Per-side data (Opening, Housing, JOH/Clearance)
    st.subheader("General Point Data")
    c1, c2 = st.columns(2)
    with c1:
        st.write("### LH Side")
        lh_opening = st.number_input("LH Opening", step=1)
        lh_housing = st.number_input("LH Housing", step=1)
        lh_jc = st.number_input(f"LH {jc_label}", step=1)
    with c2:
        st.write("### RH Side")
        rh_opening = st.number_input("RH Opening", step=1)
        rh_housing = st.number_input("RH Housing", step=1)
        rh_jc = st.number_input(f"RH {jc_label}", step=1)

    # Per-location data (Gauge, Level)
    st.subheader("Gauge & Level Measurements")
    locs = ["150 mm", "5th Sleeper", "9th Sleeper"]
    measurements = {} # To store gauge/level per location/side
    
    for loc in locs:
        st.write(f"**Location: {loc}**")
        g1, g2, l1, l2 = st.columns(4)
        measurements[(loc, "LH", "G")] = g1.number_input(f"LH Gauge ({loc})", step=1, key=f"lh_g_{loc}")
        measurements[(loc, "RH", "G")] = g2.number_input(f"RH Gauge ({loc})", step=1, key=f"rh_g_{loc}")
        measurements[(loc, "LH", "L")] = l1.number_input(f"LH Level ({loc})", step=1, key=f"lh_l_{loc}")
        measurements[(loc, "RH", "L")] = l2.number_input(f"RH Level ({loc})", step=1, key=f"rh_l_{loc}")

    remarks = st.text_area("Remarks")
    submitted = st.form_submit_button("Save Full Inspection")

# 3. Data Processing
if submitted and pt_no:
    rows = []
    for loc in locs:
        for side in ["LH", "RH"]:
            rows.append({
                "PT NO.": pt_no, "TYPE": point_type, "SIDE": side, "LOC": loc,
                "OPENING": lh_opening if side == "LH" else rh_opening,
                "HOUSING": lh_housing if side == "LH" else rh_housing,
                "JOH/CLR": lh_jc if side == "LH" else rh_jc,
                "GAUGE": measurements[(loc, side, "G")],
                "LEVEL": measurements[(loc, side, "L")],
                "REMARKS": remarks
            })
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame(rows)], ignore_index=True)
    st.success(f"Point {pt_no} saved successfully!")
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
