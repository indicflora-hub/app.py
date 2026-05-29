import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")
st.title("Joint Point & Crossing Inspection")

# 1. Initialize Session State
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["PT NO.", "SIDE", "OPENING", "HOUSING", "CLEARANCE", "REMARKS"])
if 'master_points' not in st.session_state:
    st.session_state.master_points = ["101 (TWS)", "102", "104 (TWS)", "105 (TWS)", "107", "108"]

# 2. Entry Form
st.header("Inspection Entry")
with st.form(key="inspection_form_main"):
    selected_pt = st.selectbox("Select Point No.", [""] + st.session_state.master_points, key="sel_pt")
    manual_pt = st.text_input("Or Type New Point No.", key="man_pt")
    pt_no = manual_pt if manual_pt else selected_pt
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("LH Side")
        lh_opening = st.number_input("LH Opening", step=1, key="lh_op")
        lh_housing = st.number_input("LH Housing", step=1, key="lh_ho")
        lh_clearance = st.number_input("LH Clearance", step=1, key="lh_cl")
        lh_remarks = st.text_input("LH Remarks", key="lh_re")
        
    with col2:
        st.subheader("RH Side")
        rh_opening = st.number_input("RH Opening", step=1, key="rh_op")
        rh_housing = st.number_input("RH Housing", step=1, key="rh_ho")
        rh_clearance = st.number_input("RH Clearance", step=1, key="rh_cl")
        rh_remarks = st.text_input("RH Remarks", key="rh_re")
        
    submitted = st.form_submit_button("Save Both Sides")

# 3. Data Processing
if submitted and pt_no:
    if pt_no not in st.session_state.master_points:
        st.session_state.master_points.append(pt_no)
    
    new_data = [
        {"PT NO.": pt_no, "SIDE": "LH", "OPENING": int(lh_opening), "HOUSING": int(lh_housing), "CLEARANCE": int(lh_clearance), "REMARKS": lh_remarks},
        {"PT NO.": pt_no, "SIDE": "RH", "OPENING": int(rh_opening), "HOUSING": int(rh_housing), "CLEARANCE": int(rh_clearance), "REMARKS": rh_remarks}
    ]
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame(new_data)], ignore_index=True)
    st.success(f"Data for Point {pt_no} saved!")
    st.rerun() 

# 4. Summary & Export
st.subheader("Inspection Summary")
st.session_state.data = st.data_editor(st.session_state.data, num_rows="dynamic")

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

if st.download_button("Download as Excel", data=to_excel(st.session_state.data), file_name="Joint_Point_Inspection.xlsx", mime="application/vnd.ms-excel"):
    st.success("Download ready!")

