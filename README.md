# Learner Demographics and Course Enrollment Behavior Analysis on EduPro

## Project Overview
This project presents a descriptive analytical study of learner demographics and course enrollment behavior on the EduPro online learning platform. The objective is to transform raw user, course, and transaction data into meaningful insights that support data-driven decision-making.

The project includes:
- Data cleaning and transformation
- Exploratory Data Analysis (EDA)
- Interactive Streamlit dashboard
- Deployment via Streamlit Cloud

## Objectives
- Analyze learner age distribution
- Examine gender participation patterns
- Identify popular course categories
- Study course level preferences
- Measure learner engagement concentration

## Dataset Description
The dataset consists of three sheets:

Users:
- UserID
- UserName
- Age
- Gender

Courses:
- CourseID
- CourseName
- CourseCategory
- CourseType
- CourseLevel
- CoursePrice
- CourseDuration
- CourseRating

Transactions:
- TransactionID
- UserID
- CourseID
- TransactionDate

The datasets were merged using UserID and CourseID to create a unified analytical dataset.

## Methodology
- Data Cleaning: Checked missing values and ensured data consistency
- Data Transformation: Created age groups for structured demographic analysis
- Exploratory Data Analysis: Generated visual insights using charts and heatmaps
- Dashboard Development: Built interactive dashboard using Streamlit
- Deployment: Hosted using Streamlit Cloud

## Key Insights
- Majority of learners belong to the 18–35 age group
- Beginner-level courses dominate enrollments
- Certain categories attract higher engagement
- Enrollment behavior varies across demographic segments

## Technologies Used
- Python
- Pandas
- Streamlit
- Matplotlib
- Seaborn
- Plotly
