import streamlit as st
import pandas as pd

st.set_page_config(page_title="EduPro Dashboard", layout="wide")

# Load Data
file = "data/EduPro Online Platform.xlsx"

users = pd.read_excel(file, sheet_name="Users")
courses = pd.read_excel(file, sheet_name="Courses")
transactions = pd.read_excel(file, sheet_name="Transactions")

# Merge
merged = transactions.merge(users, on="UserID").merge(courses, on="CourseID")

# Age Groups
bins = [0, 17, 25, 35, 45, 100]
labels = ["<18", "18-25", "26-35", "36-45", "45+"]
merged["AgeGroup"] = pd.cut(merged["Age"], bins=bins, labels=labels)

st.title(" EduPro Learner Demographics Dashboard")


# SIDEBAR FILTERS

st.sidebar.header("Filters")

age_filter = st.sidebar.multiselect(
    "Select Age Group",
    options=merged["AgeGroup"].unique(),
    default=merged["AgeGroup"].unique()
)

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=merged["Gender"].unique(),
    default=merged["Gender"].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Course Category",
    options=merged["CourseCategory"].unique(),
    default=merged["CourseCategory"].unique()
)

level_filter = st.sidebar.multiselect(
    "Select Course Level",
    options=merged["CourseLevel"].unique(),
    default=merged["CourseLevel"].unique()
)

filtered = merged[
    (merged["AgeGroup"].isin(age_filter)) &
    (merged["Gender"].isin(gender_filter)) &
    (merged["CourseCategory"].isin(category_filter)) &
    (merged["CourseLevel"].isin(level_filter))
]

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Total Enrollments", len(filtered))
col2.metric("Total Revenue", f"${filtered['Amount'].sum():,.2f}")
col3.metric("Average Courses per Learner",
            round(filtered.groupby("UserID").size().mean(), 2))

# VISUALS

st.subheader("Enrollments by Age Group")
st.bar_chart(filtered["AgeGroup"].value_counts())

st.subheader("Gender Distribution")
st.bar_chart(filtered["Gender"].value_counts())

st.subheader("Course Category Popularity")
st.bar_chart(filtered["CourseCategory"].value_counts())

st.subheader("Course Level Distribution")
st.bar_chart(filtered["CourseLevel"].value_counts())