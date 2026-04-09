import streamlit as st
import pandas as pd

# -------------------------------
# Title
# -------------------------------
st.title("🚨 AI Incident Intelligence Dashboard")

# -------------------------------
# Create Data (No CSV issues)
# -------------------------------
data = {
    "Incident_ID": [1, 2, 3, 4, 5],
    "Service": ["Azure Storage", "API Gateway", "Database", "Frontend App", "Backend Service"],
    "Timestamp": [
        "2026-04-01 10:00:00",
        "2026-04-01 11:30:00",
        "2026-04-01 12:15:00",
        "2026-04-01 13:00:00",
        "2026-04-01 14:45:00"
    ],
    "Severity": ["High", "Medium", "High", "Low", "Medium"],
    "Description": [
        "Storage latency spike",
        "Increased error rate",
        "Connection timeout",
        "UI misalignment",
        "Slow response time"
    ],
    "Status": ["Open", "Open", "Resolved", "Open", "Resolved"]
}

df = pd.DataFrame(data)

# -------------------------------
# Convert Timestamp
# -------------------------------
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# -------------------------------
# Add Risk Score (INTELLIGENCE)
# -------------------------------
def calculate_risk(row):
    if row["Severity"] == "High" and row["Status"] == "Open":
        return 3
    elif row["Severity"] == "Medium" and row["Status"] == "Open":
        return 2
    else:
        return 1

df["Risk_Score"] = df.apply(calculate_risk, axis=1)

# -------------------------------
# Filters
# -------------------------------
st.sidebar.header("🔍 Filters")

service_filter = st.sidebar.multiselect(
    "Select Service",
    options=df["Service"].unique(),
    default=df["Service"].unique()
)

severity_filter = st.sidebar.multiselect(
    "Select Severity",
    options=df["Severity"].unique(),
    default=df["Severity"].unique()
)

df_filtered = df[
    (df["Service"].isin(service_filter)) &
    (df["Severity"].isin(severity_filter))
]

# -------------------------------
# KPI Cards
# -------------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

total_incidents = len(df_filtered)
open_incidents = len(df_filtered[df_filtered["Status"] == "Open"])
high_severity = len(df_filtered[df_filtered["Severity"] == "High"])

col1.metric("Total Incidents", total_incidents)
col2.metric("Open Incidents", open_incidents)
col3.metric("High Severity", high_severity)

# -------------------------------
# Risk Highlight Function
# -------------------------------
def highlight_risk(row):
    if row["Risk_Score"] == 3:
        return ["background-color: #ffcccc"] * len(row)
    elif row["Risk_Score"] == 2:
        return ["background-color: #fff3cd"] * len(row)
    else:
        return ["background-color: #d4edda"] * len(row)

# -------------------------------
# High Risk Alerts
# -------------------------------
st.subheader("🚨 High Risk Incidents")

high_risk_df = df_filtered[df_filtered["Risk_Score"] == 3]

if len(high_risk_df) > 0:
    st.error(f"{len(high_risk_df)} high-risk incidents detected!")
    st.dataframe(high_risk_df)
else:
    st.success("No high-risk incidents 🎉")

# -------------------------------
# Data Table
# -------------------------------
st.subheader("📋 Incident Data")

try:
    st.dataframe(df_filtered.style.apply(highlight_risk, axis=1))
except:
    st.dataframe(df_filtered)

# -------------------------------
# AI REPORT GENERATOR
# -------------------------------
st.subheader("🤖 AI Incident Report")

if st.button("Generate AI Report"):

    total = len(df_filtered)
    open_issues = len(df_filtered[df_filtered["Status"] == "Open"])
    high_risk = len(df_filtered[df_filtered["Risk_Score"] == 3])

    # Find most affected service
    if total > 0:
        top_service = df_filtered["Service"].value_counts().idxmax()
    else:
        top_service = "N/A"

    report = f"""
    📊 Incident Summary:
    - Total Incidents: {total}
    - Open Incidents: {open_issues}
    - High Risk Incidents: {high_risk}

    🚨 Key Insight:
    - Most impacted service: {top_service}

    📌 Recommendation:
    - Prioritize high-risk open incidents immediately
    - Investigate recurring issues in critical services
    - Allocate additional resources if needed
    """

    st.text_area("AI Generated Report", report, height=250)