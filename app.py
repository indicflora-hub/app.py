import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Joint Point & Crossing Inspection")

# 1. Initialize State
if 'data' not in st.session_state:
    st.session_state.data = []

# 2. Entry/Edit Form
edit_index = st.session_state.get("edit_index", None)
with st.form(key="main_form"):
    col1, col2 = st.columns(2)
    pt_no = col1.text_input("Point No.", value=st.session_state.data[edit_index]['pt'] if edit_index is not None else "")
    p_type = col2.radio("Point Type", ["TWS", "IRS"], index=0 if edit_index is None or st.session_state.data[edit_index]['type']=="TWS" else 1, horizontal=True)
    
    jc_label = "JOH" if p_type == "TWS" else "Clearance"
    s1, s2 = st.columns(2)
    lh = {"op": s1.number_input("LH Opening", value=st.session_state.data[edit_index]['lh']['op'] if edit_index is not None else 0), 
          "ho": s1.number_input("LH Housing", value=st.session_state.data[edit_index]['lh']['ho'] if edit_index is not None else 0), 
          "jc": s1.number_input(f"LH {jc_label}", value=st.session_state.data[edit_index]['lh']['jc'] if edit_index is not None else 0)}
    rh = {"op": s2.number_input("RH Opening", value=st.session_state.data[edit_index]['rh']['op'] if edit_index is not None else 0), 
          "ho": s2.number_input("RH Housing", value=st.session_state.data[edit_index]['rh']['ho'] if edit_index is not None else 0), 
          "jc": s2.number_input(f"RH {jc_label}", value=st.session_state.data[edit_index]['rh']['jc'] if edit_index is not None else 0)}
    
    loc_inputs = {}
    for loc in ["150 MM", "5TH SLEEPER", "9TH SLEEPER"]:
        g, l = st.columns(2)
        v = st.session_state.data[edit_index]['locs'][loc] if edit_index is not None else {'g':'', 'l':''}
        loc_inputs[loc] = {"g": g.text_input(f"Gauge {loc}", value=v['g']), "l": l.text_input(f"Level {loc}", value=v['l'])}
    
    remarks = st.text_area("Remarks", value=st.session_state.data[edit_index]['rem'] if edit_index is not None else "")
    submitted = st.form_submit_button("Save Changes" if edit_index is not None else "Add Entry")

if submitted:
    entry = {"pt": pt_no, "type": p_type, "lh": lh, "rh": rh, "locs": loc_inputs, "rem": remarks}
    if edit_index is not None: st.session_state.data[edit_index] = entry
    else: st.session_state.data.append(entry)
    st.session_state["edit_index"] = None
    st.rerun()

# 3. View Window with Scrollable Container
st.subheader("Inspection Records View")
search = st.text_input("🔍 Search Point No.")

# This container acts as the 'view window' with a scroll bar if data is long
with st.container(height=400): 
    for i, entry in enumerate(st.session_state.data):
        if search.lower() in entry['pt'].lower():
            cols = st.columns([0.6, 0.2, 0.2])
            cols[0].write(f"**Point {entry['pt']}** ({entry['type']})")
            if cols[1].button("Edit", key=f"e{i}"):
                st.session_state["edit_index"] = i
                st.rerun()
            if cols[2].button("Delete", key=f"d{i}"):
                st.session_state.data.pop(i)
                st.rerun()
            st.divider()
