import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

st.set_page_config(layout="wide")
st.title("Joint Point & Crossing Inspection")

# 1. Initialize State
if 'data' not in st.session_state:
    st.session_state.data = []

# Function to clear form
def clear_form():
    st.session_state["edit_index"] = None

# 2. Edit/Add Toggle
edit_index = st.session_state.get("edit_index", None)
mode = "Edit Entry" if edit_index is not None else "New Entry"
st.header(mode)

# Load data for editing if an index is selected
default_data = st.session_state.data[edit_index] if edit_index is not None else None

with st.form(key="main_form"):
    col1, col2 = st.columns(2)
    pt_no = col1.text_input("Point No.", value=default_data['pt'] if default_data else "")
    p_type = col2.radio("Point Type", ["TWS", "IRS"], index=0 if not default_data or default_data['type']=="TWS" else 1, horizontal=True)
    
    jc_label = "JOH" if p_type == "TWS" else "Clearance"
    
    s1, s2 = st.columns(2)
    lh = {"op": s1.number_input("LH Opening", value=default_data['lh']['op'] if default_data else 0), 
          "ho": s1.number_input("LH Housing", value=default_data['lh']['ho'] if default_data else 0), 
          "jc": s1.number_input(f"LH {jc_label}", value=default_data['lh']['jc'] if default_data else 0)}
    rh = {"op": s2.number_input("RH Opening", value=default_data['rh']['op'] if default_data else 0), 
          "ho": s2.number_input("RH Housing", value=default_data['rh']['ho'] if default_data else 0), 
          "jc": s2.number_input(f"RH {jc_label}", value=default_data['rh']['jc'] if default_data else 0)}
    
    st.write("---")
    locs = ["150 MM", "5TH SLEEPER", "9TH SLEEPER"]
    loc_inputs = {}
    for loc in locs:
        g, l = st.columns(2)
        val_g = default_data['locs'][loc]['g'] if default_data else ""
        val_l = default_data['locs'][loc]['l'] if default_data else ""
        loc_inputs[loc] = {"g": g.text_input(f"Gauge {loc}", value=val_g), "l": l.text_input(f"Level {loc}", value=val_l)}
    
    remarks = st.text_area("Remarks", value=default_data['rem'] if default_data else "")
    submitted = st.form_submit_button("Save Changes" if edit_index is not None else "Add Entry")

if submitted:
    new_entry = {"pt": pt_no, "type": p_type, "lh": lh, "rh": rh, "locs": loc_inputs, "rem": remarks}
    if edit_index is not None:
        st.session_state.data[edit_index] = new_entry
        st.session_state["edit_index"] = None
    else:
        st.session_state.data.append(new_entry)
    st.rerun()

# 3. List view for selection
st.subheader("Saved Records")
for i, entry in enumerate(st.session_state.data):
    c1, c2 = st.columns([0.8, 0.2])
    c1.write(f"Point {entry['pt']} - {entry['type']}")
    if c2.button("Edit", key=f"edit_{i}"):
        st.session_state["edit_index"] = i
        st.rerun()
