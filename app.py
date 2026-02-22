import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EduPro Dashboard", layout="wide")

@st.cache_data
def load_data():
    file = "data/EduPro Online Platform.xlsx"
    users = pd.read_excel(file, sheet_name="Users")
    courses = pd.read_excel(file, sheet_name="Courses")
    transactions = pd.read_excel(file, sheet_name="Transactions")
    return users, courses, transactions

users, courses, transactions = load_data()
merged = transactions.merge(users, on="UserID").merge(courses, on="CourseID")

bins = [0, 17, 25, 35, 45, 100]
labels = ["<18", "18-25", "26-35", "36-45", "45+"]
merged["AgeGroup"] = pd.cut(merged["Age"], bins=bins, labels=labels)

st.title("EduPro Learner Demographics Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
age_filter = st.sidebar.multiselect("Age Group", options=merged["AgeGroup"].unique(), default=merged["AgeGroup"].unique())
gender_filter = st.sidebar.multiselect("Gender", options=merged["Gender"].unique(), default=merged["Gender"].unique())
category_filter = st.sidebar.multiselect("Course Category", options=merged["CourseCategory"].unique(), default=merged["CourseCategory"].unique())
level_filter = st.sidebar.multiselect("Course Level", options=merged["CourseLevel"].unique(), default=merged["CourseLevel"].unique())

filtered = merged[
    (merged["AgeGroup"].isin(age_filter)) &
    (merged["Gender"].isin(gender_filter)) &
    (merged["CourseCategory"].isin(category_filter)) &
    (merged["CourseLevel"].isin(level_filter))
]

# KPIs (slightly polished but simple)
col1, col2, col3 = st.columns(3)
col1.metric("Total Enrollments", len(filtered))
col2.metric("Total Revenue", f"${filtered['Amount'].sum():,.2f}")
col3.metric("Avg Courses per Learner", round(filtered.groupby("UserID").size().mean(), 2))

# Charts with Plotly (cleaner than st.bar_chart but not overcomplicated)
st.subheader("Enrollments by Age Group")
age_fig = px.bar(filtered["AgeGroup"].value_counts().reset_index(),
                 x="index", y="AgeGroup",
                 labels={"index": "Age Group", "AgeGroup": "Enrollments"},
                 title="Enrollments by Age Group")
st.plotly_chart(age_fig, use_container_width=True)

st.subheader("Gender Distribution")
gender_fig = px.pie(filtered, names="Gender", title="Gender Distribution")
st.plotly_chart(gender_fig, use_container_width=True)

st.subheader("Course Category Popularity")
category_fig = px.bar(filtered["CourseCategory"].value_counts().reset_index(),
                      x="index", y="CourseCategory",
                      labels={"index": "Course Category", "CourseCategory": "Enrollments"},
                      title="Course Category Popularity")
st.plotly_chart(category_fig, use_container_width=True)

st.subheader("Course Level Distribution")
level_fig = px.bar(filtered["CourseLevel"].value_counts().reset_index(),
                   x="index", y="CourseLevel",
                   labels={"index": "Course Level", "CourseLevel": "Enrollments"},
                   title="Course Level Distribution")
st.plotly_chart(level_fig, use_container_width=True)
