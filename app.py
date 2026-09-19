import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Manufacturing Time Analyzer",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Manufacturing Time Analyzer")
st.caption("Analyze where manufacturing time is being spent.")

# Load data
uploaded_file = st.sidebar.file_uploader(
    "Upload Manufacturing CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("sample_manufacturing_data.csv")

# Check columns
required_columns = [
    "Process",
    "Activity",
    "Duration (min)",
    "Time Type",
    "Reason"
]

missing = [c for c in required_columns if c not in df.columns]

if missing:
    st.error("Missing columns: " + ", ".join(missing))
    st.stop()

# Clean duration
df["Duration (min)"] = pd.to_numeric(
    df["Duration (min)"],
    errors="coerce"
).fillna(0)

# Calculations
total_time = df["Duration (min)"].sum()

processing_time = df.loc[
    df["Time Type"] == "Processing",
    "Duration (min)"
].sum()

non_processing_time = total_time - processing_time

non_processing_percentage = (
    non_processing_time / total_time * 100
    if total_time > 0 else 0
)

# KPI section
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Time", f"{total_time:.0f} min")
col2.metric("Processing Time", f"{processing_time:.0f} min")
col3.metric("Non-Processing / Review", f"{non_processing_time:.0f} min")
col4.metric("Non-Processing %", f"{non_processing_percentage:.1f}%")

# Time type
st.subheader("1️⃣ Time by Activity Type")

time_by_type = (
    df.groupby("Time Type")["Duration (min)"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(time_by_type)

# Process
st.subheader("2️⃣ Time by Manufacturing Process")

time_by_process = (
    df.groupby("Process")["Duration (min)"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(time_by_process)

# Non-processing analysis
st.subheader("3️⃣ Non-Processing / Review Analysis")

non_processing_df = df[
    df["Time Type"] != "Processing"
]

if not non_processing_df.empty:

    category_analysis = (
        non_processing_df
        .groupby("Time Type")["Duration (min)"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_analysis)

# Top candidates
st.subheader("4️⃣ Top Time-Loss / Review Candidates")

if not non_processing_df.empty:

    top_candidates = (
        non_processing_df
        .groupby(
            ["Time Type", "Reason"],
            as_index=False
        )["Duration (min)"]
        .sum()
        .sort_values(
            "Duration (min)",
            ascending=False
        )
    )

    st.dataframe(
        top_candidates,
        width="stretch",
        hide_index=True
    )

# Full data
st.subheader("5️⃣ Manufacturing Time Records")

st.dataframe(
    df,
    width="stretch",
    hide_index=True
)

# Download
st.download_button(
    "⬇️ Download Analyzed CSV",
    df.to_csv(index=False).encode("utf-8"),
    "manufacturing_time_analysis.csv",
    "text/csv"
)

st.caption(
    "MVP note: Time classification should be validated and refined "
    "using real manufacturing data."
)
