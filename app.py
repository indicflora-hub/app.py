import streamlit as st
import pandas as pd
from fpdf import FPDF

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Joint Point & Crossing Inspection",
    layout="wide"
)

st.title("Joint Point & Crossing Inspection System")

# ---------------------------------------------------
# SESSION STORAGE
# ---------------------------------------------------
if "data" not in st.session_state:
    st.session_state.data = []

# ---------------------------------------------------
# ENTRY FORM
# ---------------------------------------------------
st.header("Enter Inspection Details")

with st.form("inspection_form"):

    # Basic Details
    c1, c2 = st.columns(2)

    point_no = c1.text_input("Point No.")

    point_type = c2.radio(
        "Type",
        ["TWS", "IRS"],
        horizontal=True
    )

    label_name = "JOH" if point_type == "TWS" else "Clearance"

    # ---------------------------------------------------
    # LH & RH DETAILS
    # ---------------------------------------------------
    st.subheader("Measurement Details")

    col_lh, col_rh = st.columns(2)

    with col_lh:
        st.markdown("### LH Side")

        lh_opening = st.number_input(
            "LH Opening",
            min_value=0.0,
            format="%.2f"
        )

        lh_horizontal = st.number_input(
            "LH Horizontal",
            min_value=0.0,
            format="%.2f"
        )

        lh_joh = st.number_input(
            f"LH {label_name}",
            min_value=0.0,
            format="%.2f"
        )

    with col_rh:
        st.markdown("### RH Side")

        rh_opening = st.number_input(
            "RH Opening",
            min_value=0.0,
            format="%.2f"
        )

        rh_horizontal = st.number_input(
            "RH Horizontal",
            min_value=0.0,
            format="%.2f"
        )

        rh_joh = st.number_input(
            f"RH {label_name}",
            min_value=0.0,
            format="%.2f"
        )

    # ---------------------------------------------------
    # GAUGE & LEVEL
    # ---------------------------------------------------
    st.subheader("Gauge & Level")

    locations = [
        "150 MM",
        "5TH SLEEPER",
        "9TH SLEEPER"
    ]

    gauge_level_data = {}

    for loc in locations:

        g_col, l_col = st.columns(2)

        gauge = g_col.text_input(f"Gauge at {loc}")

        level = l_col.text_input(f"Level at {loc}")

        gauge_level_data[loc] = {
            "gauge": gauge,
            "level": level
        }

    # ---------------------------------------------------
    # REMARKS
    # ---------------------------------------------------
    remarks = st.text_area("Remarks")

    # ---------------------------------------------------
    # SAVE BUTTON
    # ---------------------------------------------------
    submitted = st.form_submit_button("Save Record")

    if submitted:

        record = {
            "Point No": point_no,
            "Type": point_type,

            "LH Opening": lh_opening,
            "LH Horizontal": lh_horizontal,
            f"LH {label_name}": lh_joh,

            "RH Opening": rh_opening,
            "RH Horizontal": rh_horizontal,
            f"RH {label_name}": rh_joh,

            "Gauge_Level": gauge_level_data,

            "Remarks": remarks
        }

        st.session_state.data.append(record)

        st.success("Record Saved Successfully")

# ---------------------------------------------------
# DISPLAY RECORDS
# ---------------------------------------------------
st.header("Saved Records")

if len(st.session_state.data) == 0:

    st.info("No records available.")

else:

    for i, record in enumerate(st.session_state.data):

        with st.expander(
            f"Point No: {record['Point No']} | Type: {record['Type']}",
            expanded=False
        ):

            c1, c2 = st.columns(2)

            # LH Details
            with c1:
                st.markdown("### LH Details")

                st.write(
                    f"Opening : {record['LH Opening']}"
                )

                st.write(
                    f"Horizontal : {record['LH Horizontal']}"
                )

                key_lh = [
                    k for k in record.keys()
                    if "LH JOH" in k or "LH Clearance" in k
                ][0]

                st.write(
                    f"{key_lh} : {record[key_lh]}"
                )

            # RH Details
            with c2:
                st.markdown("### RH Details")

                st.write(
                    f"Opening : {record['RH Opening']}"
                )

                st.write(
                    f"Horizontal : {record['RH Horizontal']}"
                )

                key_rh = [
                    k for k in record.keys()
                    if "RH JOH" in k or "RH Clearance" in k
                ][0]

                st.write(
                    f"{key_rh} : {record[key_rh]}"
                )

            # Gauge & Level
            st.markdown("### Gauge & Level")

            for loc, values in record["Gauge_Level"].items():

                st.write(
                    f"{loc} → Gauge: {values['gauge']} | "
                    f"Level: {values['level']}"
                )

            # Remarks
            st.markdown("### Remarks")

            st.write(record["Remarks"])

            # Delete Button
            if st.button(
                f"Delete Record {i+1}",
                key=f"delete_{i}"
            ):

                st.session_state.data.pop(i)

                st.rerun()

# ---------------------------------------------------
# DATAFRAME VIEW
# ---------------------------------------------------
st.header("Tabular View")

if st.session_state.data:

    table_data = []

    for rec in st.session_state.data:

        row = {
            "Point No": rec["Point No"],
            "Type": rec["Type"],
            "LH Opening": rec["LH Opening"],
            "RH Opening": rec["RH Opening"],
            "Remarks": rec["Remarks"]
        }

        table_data.append(row)

    df = pd.DataFrame(table_data)

    st.dataframe(
        df,
        use_container_width=True
    )

# ---------------------------------------------------
# PDF GENERATION
# ---------------------------------------------------
def create_pdf(records):

    pdf = FPDF()

    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()

    pdf.set_font("Arial", "B", 16)

    pdf.cell(
        200,
        10,
        txt="Joint Point & Crossing Inspection Report",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    for rec in records:

        pdf.set_font("Arial", "B", 12)

        pdf.cell(
            200,
            8,
            txt=f"Point No: {rec['Point No']} ({rec['Type']})",
            ln=True
        )

        pdf.set_font("Arial", "", 10)

        pdf.cell(
            200,
            7,
            txt=f"LH Opening: {rec['LH Opening']}",
            ln=True
        )

        pdf.cell(
            200,
            7,
            txt=f"RH Opening: {rec['RH Opening']}",
            ln=True
        )

        pdf.cell(
            200,
            7,
            txt=f"Remarks: {rec['Remarks']}",
            ln=True
        )

        pdf.ln(5)

    return pdf.output(dest="S").encode("latin-1")

# ---------------------------------------------------
# DOWNLOAD PDF
# ---------------------------------------------------
if st.session_state.data:

    pdf_file = create_pdf(st.session_state.data)

    st.download_button(
        label="Download PDF Report",
        data=pdf_file,
        file_name="Joint_Inspection_Report.pdf",
        mime="application/pdf"
    )
