import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

st.set_page_config(layout="wide")
st.title("Rail Inspection Logger")

# Initialize Data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["PT NO.", "SIDE", "OPENING", "HOUSING", "CLEARANCE", "REMARKS"])
if 'master_points' not in st.session_state:
    st.session_state.master_points = ["101 (TWS)", "102", "104 (TWS)", "105 (TWS)", "107", "108"]

# Entry Form
st.header("Inspection Entry")
with st.form("inspection_form"):
    pt_no = st.selectbox("Select Point No.", st.session_state.master_points)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("LH Side")
        lh_opening = st.number_input("LH Opening", key="lh_op")
        lh_housing = st.number_input("LH Housing", key="lh_ho")
        lh_clearance = st.number_input("LH Clearance", key="lh_cl")
        lh_remarks = st.text_input("LH Remarks", key="lh_re")
        
    with col2:
        st.subheader("RH Side")
        rh_opening = st.number_input("RH Opening", key="rh_op")
        rh_housing = st.number_input("RH Housing", key="rh_ho")
        rh_clearance = st.number_input("RH Clearance", key="rh_cl")
        rh_remarks = st.text_input("RH Remarks", key="rh_re")
        
    submitted = st.form_submit_button("Save Both Sides")

if submitted:
    new_data = [
        {"PT NO.": pt_no, "SIDE": "LH", "OPENING": lh_opening, "HOUSING": lh_housing, "CLEARANCE": lh_clearance, "REMARKS": lh_remarks},
        {"PT NO.": pt_no, "SIDE": "RH", "OPENING": rh_opening, "HOUSING": rh_housing, "CLEARANCE": rh_clearance, "REMARKS": rh_remarks}
    ]
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame(new_data)], ignore_index=True)
    st.success(f"Data for Point {pt_no} saved successfully!")

# Summary Table
st.subheader("Inspection Summary")
st.session_state.data = st.data_editor(st.session_state.data, num_rows="dynamic")

# Excel/PDF Export logic remains the same as before...
import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

st.set_page_config(layout="wide")
st.title("Rail Inspection Logger")

# 1. Initialization
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["PT NO.", "SIDE", "OPENING", "HOUSING", "CLEARANCE", "REMARKS"])
if 'master_points' not in st.session_state:
    st.session_state.master_points = ["101 (TWS)", "102", "104 (TWS)", "105 (TWS)", "107", "108"]

# 2. Entry Form
with st.sidebar:
    st.header("Inspection Input")
    with st.form("entry_form"):
        pt_no = st.selectbox("Select Point No.", st.session_state.master_points)
        side = st.selectbox("Side", ["LH", "RH"])
        opening = st.number_input("Opening")
        housing = st.number_input("Housing")
        clearance = st.number_input("Clearance")
        remarks = st.text_area("Remarks")
        
        # Optional Camera Input
        photo = st.camera_input("Take a photo of the defect (Optional)")
        
        submitted = st.form_submit_button("Save Entry")

if submitted:
    new_row = {"PT NO.": pt_no, "SIDE": side, "OPENING": opening, "HOUSING": housing, "CLEARANCE": clearance, "REMARKS": remarks}
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)

# 3. Summary & Export
st.subheader("Inspection Summary")
st.session_state.data = st.data_editor(st.session_state.data, num_rows="dynamic")

# Excel Export Function
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# Layout for Export Buttons
col1, col2 = st.columns(2)

with col1:
    excel_data = to_excel(st.session_state.data)
    st.download_button("Download as Excel", data=excel_data, file_name="inspection_log.xlsx", mime="application/vnd.ms-excel")

with col2:
    if st.button("Generate PDF Summary"):
        # (PDF logic from previous step remains here)
        st.success("PDF Generated!")

