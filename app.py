# Updated Streamlit Code – Joint Point & Crossing Inspection

```python
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

    # ---------------------------------------------
    # BASIC DETAILS
    # ---------------------------------------------
    c1, c2 = st.columns(2)

    point_no = c1.text_input("Point No.")

    point_type = c2.radio(
        "Type",
        ["TWS", "IRS"],
        horizontal=True
    )

    label_name = "JOH" if point_type == "TWS" else "Clearance"

    # ---------------------------------------------
    # LH & RH DETAILS
    # ---------------------------------------------
    st.subheader("Measurement Details")

    col_lh, col_rh = st.columns(2)

    # LH SIDE
    with col_lh:

        st.markdown("### LH Side")

        lh_opening = st.number_input(
            "LH Opening",
            min_value=0,
            step=1,
            format="%d"
        )

        lh_housing = st.number_input(
            "LH Housing",
            min_value=0,
            step=1,
            format="%d",
            key="lh_housing"
        )

        lh_joh = st.number_input(
            f"LH {label_name}",
            min_value=0,
            step=1,
            format="%d"
        )

    # RH SIDE
    with col_rh:

        st.markdown("### RH Side")

        rh_opening = st.number_input(
            "RH Opening",
            min_value=0,
            step=1,
            format="%d"
        )

        rh_housing = st.number_input(
            "RH Housing",
            min_value=0,
            step=1,
            format="%d",
            key="rh_housing"
        )

        rh_joh = st.number_input(
            f"RH {label_name}",
            min_value=0,
            step=1,
            format="%d"
        )

    # ---------------------------------------------
    # GAUGE & LEVEL
    # ---------------------------------------------
    st.subheader("Gauge & Level")

    locations = [
        "150 MM",
        "5TH SLEEPER",
        "9TH SLEEPER"
    ]

    gauge_level_data = {}

    for loc in locations:

        c1, c2 = st.columns(2)

        gauge = c1.text_input(
            f"Gauge at {loc}",
            placeholder="Example: EXACT, -5, +3"
        )

        level = c2.text_input(
            f"Level at {loc}",
            placeholder="Example: 7LL, 3RL"
        )

        gauge_level_data[loc] = {
            "gauge": gauge,
            "level": level
        }

    # ---------------------------------------------
    # REMARKS
    # ---------------------------------------------
    remarks = st.text_area("Remarks")

    # ---------------------------------------------
    # SAVE BUTTON
    # ---------------------------------------------
    save = st.form_submit_button("Save Record")

    if save:

        record = {
            "Point No": point_no,
            "Type": point_type,

            "LH Opening": lh_opening,
            "LH Housing": lh_housing,
            f"LH {label_name}": lh_joh,

            "RH Opening": rh_opening,
            "RH Housing": rh_housing,
            f"RH {label_name}": rh_joh,

            "Gauge_Level": gauge_level_data,

            "Remarks": remarks
        }

        st.session_state.data.append(record)

        st.success("Record Saved Successfully")

# -------------------------------------------------
# DISPLAY SAVED RECORDS
# -------------------------------------------------
st.header("Saved Records")

if not st.session_state.data:

    st.info("No records available")

else:

    for i, rec in enumerate(st.session_state.data):

        with st.expander(
            f"Point No: {rec['Point No']} | Type: {rec['Type']}",
            expanded=False
        ):

            c1, c2 = st.columns(2)

            # LH DETAILS
            with c1:

                st.markdown("### LH Details")

                st.write(f"Opening : {rec['LH Opening']}")
                st.write(f"Housing : {rec['LH Housing']}")

                lh_key = [
                    k for k in rec.keys()
                    if "LH JOH" in k or "LH Clearance" in k
                ][0]

                st.write(f"{lh_key} : {rec[lh_key]}")

            # RH DETAILS
            with c2:

                st.markdown("### RH Details")

                st.write(f"Opening : {rec['RH Opening']}")
                st.write(f"Housing : {rec['RH Housing']}")

                rh_key = [
                    k for k in rec.keys()
                    if "RH JOH" in k or "RH Clearance" in k
                ][0]

                st.write(f"{rh_key} : {rec[rh_key]}")

            # GAUGE LEVEL
            st.markdown("### Gauge & Level")

            for loc, values in rec["Gauge_Level"].items():

                st.write(
                    f"{loc} → Gauge: {values['gauge']} | Level: {values['level']}"
                )

            # REMARKS
            st.markdown("### Remarks")
            st.write(rec["Remarks"])

            # DELETE BUTTON
            if st.button(
                f"Delete Record {i+1}",
                key=f"delete_{i}"
            ):

                st.session_state.data.pop(i)
                st.rerun()

# -------------------------------------------------
# TABULAR VIEW
# -------------------------------------------------
st.header("Tabular View")

if st.session_state.data:

    rows = []

    for rec in st.session_state.data:

        rows.append({
            "Point No": rec["Point No"],
            "Type": rec["Type"],
            "LH Opening": rec["LH Opening"],
            "RH Opening": rec["RH Opening"],
            "Remarks": rec["Remarks"]
        })

    df = pd.DataFrame(rows)

    st.dataframe(df, use_container_width=True)

# -------------------------------------------------
# PDF CREATION
# -------------------------------------------------
def create_pdf(records):

    pdf = FPDF()

    pdf.set_auto_page_break(auto=True, margin=10)

    pdf.add_page()

    # TITLE
    pdf.set_font("Arial", "B", 14)

    pdf.cell(
        190,
        10,
        "JOINT POINT & CROSSING INSPECTION",
        border=1,
        ln=True,
        align="C"
    )

    pdf.ln(5)

    # HEADER ROW
    pdf.set_font("Arial", "B", 9)

    headers = [
        "PT NO.",
        "SIDE",
        "OPENING",
        "HOUSING",
        "CLEAR./JOH",
        "GAUGE LOCATION",
        "GAUGE",
        "LEVEL LOCATION",
        "LEVEL"
    ]

    widths = [18, 12, 18, 18, 22, 25, 15, 25, 15]

    for h, w in zip(headers, widths):
        pdf.cell(w, 10, h, border=1, align="C")

    pdf.ln()

    # DATA ROWS
    pdf.set_font("Arial", "", 8)

    for rec in records:

        # LH KEY
        lh_key = [
            k for k in rec.keys()
            if "LH JOH" in k or "LH Clearance" in k
        ][0]

        # RH KEY
        rh_key = [
            k for k in rec.keys()
            if "RH JOH" in k or "RH Clearance" in k
        ][0]

        locations = list(rec["Gauge_Level"].keys())

        # -----------------------------------------
        # LH ROW
        # -----------------------------------------
        pdf.cell(18, 10, str(rec['Point No']), border=1)
        pdf.cell(15, 10, "LH", border=1, align="C")
        pdf.cell(20, 10, str(rec['LH Opening']), border=1, align="C")
        pdf.cell(20, 10, str(rec['LH Housing']), border=1, align="C")
        pdf.cell(25, 10, str(rec[lh_key]), border=1, align="C")

        pdf.cell(30, 10, locations[0], border=1)
        pdf.cell(15, 10, str(rec['Gauge_Level'][locations[0]]['gauge']), border=1, align="C")

        pdf.cell(30, 10, locations[0], border=1)
        pdf.cell(15, 10, str(rec['Gauge_Level'][locations[0]]['level']), border=1, align="C")

        pdf.ln()

        # -----------------------------------------
        # RH ROW
        # -----------------------------------------
        pdf.cell(20, 10, "", border=1)
        pdf.cell(15, 10, "RH", border=1, align="C")
        pdf.cell(20, 10, str(rec['RH Opening']), border=1, align="C")
        pdf.cell(20, 10, str(rec['RH Housing']), border=1, align="C")
        pdf.cell(25, 10, str(rec[rh_key]), border=1, align="C")

        pdf.cell(30, 10, locations[1], border=1)
        pdf.cell(15, 10, str(rec['Gauge_Level'][locations[1]]['gauge']), border=1, align="C")

        pdf.cell(30, 10, locations[1], border=1)
        pdf.cell(15, 10, str(rec['Gauge_Level'][locations[1]]['level']), border=1, align="C")

        pdf.ln()

        # -----------------------------------------
        # 3RD ROW
        # -----------------------------------------
        pdf.cell(20, 10, "", border=1)
        pdf.cell(15, 10, "", border=1)
        pdf.cell(20, 10, "", border=1)
        pdf.cell(20, 10, "", border=1)
        pdf.cell(25, 10, "", border=1)

        pdf.cell(30, 10, locations[2], border=1)
        pdf.cell(15, 10, str(rec['Gauge_Level'][locations[2]]['gauge']), border=1, align="C")

        pdf.cell(30, 10, locations[2], border=1)
        pdf.cell(15, 10, str(rec['Gauge_Level'][locations[2]]['level']), border=1, align="C")

        pdf.ln()

        # EMPTY GAP ROW
        for w in widths:
            pdf.cell(w, 7, "", border=1)

        pdf.ln()

        # REMARKS
        if rec['Remarks']:

            pdf.cell(
                190,
                8,
                f"Remarks: {rec['Remarks']}",
                border=1,
                ln=True
            )

    return pdf.output(dest="S").encode("latin-1")

# -------------------------------------------------
# DOWNLOAD PDF
# -------------------------------------------------
if st.session_state.data:

    pdf_file = create_pdf(st.session_state.data)

    st.download_button(
        label="Download PDF Report",
        data=pdf_file,
        file_name="Joint_Point_Crossing_Report.pdf",
        mime="application/pdf"
    )

```

## Main Changes Done

### 1. Whole Number Entry

All measurement fields now accept only integer values.

### 2. Gauge & Level Supports

These fields now support:

* Alphabets
* Numbers
* Symbols
* EXACT
* * / - values
* LL / RL etc.

### 3. PDF Format Updated

PDF layout now follows your uploaded Excel sheet style:

* PT NO.
* SIDE
* OPENING
* HOUSING
* CLEARANCE / JOH
* GAUGE
* LEVEL
* Multi-row format
* Table structure similar to Excel

### 4. Better Screen Display

Saved records now display properly using expandable sections.
