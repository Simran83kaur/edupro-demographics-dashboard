import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="EduPro Analytics", layout="wide")

st.title("🎓 EduPro Learner Intelligence Dashboard")
st.markdown("Interactive analysis of learner demographics and course enrollment behavior")

# =========================
# LOAD DATA
# =========================
file = "data/EduPro Online Platform.xlsx"

users = pd.read_excel(file, sheet_name="Users")
courses = pd.read_excel(file, sheet_name="Courses")
transactions = pd.read_excel(file, sheet_name="Transactions")

filtered_data = transactions.merge(users, on="UserID")
filtered_data = filtered_data.merge(courses, on="CourseID")

# Age Groups
bins = [0, 17, 25, 35, 45, 100]
labels = ["<18", "18-25", "26-35", "36-45", "45+"]
filtered_data["AgeGroup"] = pd.cut(filtered_data["Age"], bins=bins, labels=labels)

#SIDEBAR
st.sidebar.markdown("## 🎛 Dashboard Filters")
st.sidebar.markdown("---")

with st.sidebar.expander("👥 Demographics Filters", expanded=True):
    age_filter = st.multiselect(
        "Age Group",
        sorted(filtered_data["AgeGroup"].dropna().unique()),
        default=filtered_data["AgeGroup"].dropna().unique()
    )

    gender_filter = st.multiselect(
        "Gender",
        filtered_data["Gender"].unique(),
        default=filtered_data["Gender"].unique()
    )

with st.sidebar.expander("📚 Course Filters", expanded=True):
    category_filter = st.multiselect(
        "Course Category",
        filtered_data["CourseCategory"].unique(),
        default=filtered_data["CourseCategory"].unique()
    )

    level_filter = st.multiselect(
        "Course Level",
        filtered_data["CourseLevel"].unique(),
        default=filtered_data["CourseLevel"].unique()
    )
    
# =========================
# APPLY FILTERS
# =========================

filtered_data["AgeGroup"] = filtered_data["AgeGroup"].astype(str)

filtered_data = filtered_data.copy()

if age_filter:
    filtered_data = filtered_data[filtered_data["AgeGroup"].isin(age_filter)]

if gender_filter:
    filtered_data = filtered_data[filtered_data["Gender"].isin(gender_filter)]

if category_filter:
    filtered_data = filtered_data[filtered_data["CourseCategory"].isin(category_filter)]

if level_filter:
    filtered_data = filtered_data[filtered_data["CourseLevel"].isin(level_filter)]    

# =========================
# KPI SECTION
# =========================
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Enrollments", filtered_data.shape[0])
col2.metric("Unique Learners", filtered_data["UserID"].nunique())
col3.metric("Avg Courses / Learner",
            round(filtered_data.groupby("UserID").size().mean(), 2))
col4.metric("Free Course %",
            round((filtered_data["CourseType"] == "Free").mean()*100, 1))

st.markdown("---")

# =========================
# ROW 1: CATEGORY + LEVEL
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📚 Course Category Distribution")
    fig_cat = px.bar(
        filtered_data["CourseCategory"].value_counts().reset_index(),
        x="CourseCategory",
        y="count",
        labels={"count": "Enrollments"},
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col2:
    st.subheader("🎯 Course Level Distribution")
    fig_level = px.pie(
        filtered_data,
        names="CourseLevel",
        title="Level Share"
    )
    st.plotly_chart(fig_level, use_container_width=True)

st.markdown("---")

# =========================
# ROW 2: GENDER + AGE
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("👩‍🎓 Gender Distribution")
    fig_gender = px.bar(
        filtered_data["Gender"].value_counts().reset_index(),
        x="Gender",
        y="count"
    )
    st.plotly_chart(fig_gender, use_container_width=True)

with col2:
    st.subheader("📈 Age Group Distribution")
    fig_age = px.bar(
        filtered_data["AgeGroup"].value_counts().reset_index(),
        x="AgeGroup",
        y="count"
    )
    st.plotly_chart(fig_age, use_container_width=True)

st.markdown("---")

# =========================
# HEATMAP
# =========================
st.subheader("🔥 Age Group vs Course Category Heatmap")

heatmap_data = pd.crosstab(
    filtered_data["AgeGroup"],
    filtered_data["CourseCategory"]
)

fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", ax=ax)
st.pyplot(fig)

st.markdown("---")

# =========================
# LEARNER SEGMENTATION
# =========================
st.subheader("👥 Learner Segmentation")

courses_per_user = filtered_data.groupby("UserID").size()

segments = pd.cut(
    courses_per_user,
    bins=[0, 1, 3, 100],
    labels=["Single Course", "Moderate Learner", "Power Learner"]
)

fig_seg = px.bar(
    segments.value_counts().reset_index(),
    x="index",
    y="count",
    labels={"index": "Segment"}
)

st.plotly_chart(fig_seg, use_container_width=True)