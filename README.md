![CI](https://github.com/Aymane170/FakeSchoolData/actions/workflows/run_analysis.yml/badge.svg)



# **FakeSchoolData**
A fully automated data pipeline that simulates school data, loads it into a Snowflake data warehouse, transforms it with dbt, and analyzes it with Python—generating visual insights and storing them in GitHub Actions Artifacts.

## Project Overview
FakeSchoolData is a personal data engineering project designed to simulate and analyze academic data for a fictional school. It covers the entire data lifecycle, from generation to analysis, while showcasing modern data stack tools and automation.

## Tech Stack
    Languages: Python 3.10, SQL

    Libraries: pandas, matplotlib, faker, snowflake-connector-python

    Data Warehouse: Snowflake

    Transformation Tool: dbt (Data Build Tool)

    CI/CD: GitHub Actions

    Version Control: Git

# Repository Structure

    FakeSchoolData/
    ├── .github/
    │   └── workflows/
    │       └── run_analysis.yml           # GitHub Actions CI/CD pipeline
    ├── analyze_results.py                 # Analysis and visualization script
    ├── average_grades_chart.png          # Generated chart (uploaded as artifact)
    ├── courses.csv                       # Simulated course data
    ├── generate_data.py                  # Script for data generation
    ├── log/                              # Log files
    ├── results.csv                       # Simulated grade data
    ├── students.csv                      # Simulated student data
    ├── venv/                             # Virtual environment (not versioned)
    ├── .gitignore
    ├── fakeschool_dbt/                   # dbt transformation project
    │   └── models/
    │       ├── average_grades.py         # Model for average grades per course
    │       ├── top_students.py           # Model for top students
    │       └── schema.yml                # Model documentation and tests
# Workflow Summary
## 1. Data Generation (generate_data.py)
    Generates:

    100 students (ID, first name, last name)

    10 courses (ID, name)

    Random results (grades between 0 and 20) per student per course

    Output:
    students.csv, courses.csv, results.csv

## 2. Load to Snowflake
    Connects to Snowflake using snowflake-connector-python

    Creates RAW schema with tables: STUDENTS, COURSES, RESULTS

    Uses internal staging and COPY INTO to bulk load data

## 3. Transform Data with dbt
    Initializes dbt project: fakeschool_dbt

    Models:

    average_grades.py: Calculates average grade per course

    top_students.py: Extracts top 5 students by GPA

    Uses schema.yml for model validation

    Run with dbt run

## 4. Analyze Results (analyze_results.py)
    Connects to Snowflake and queries transformed tables

    Computes:

    Average, median, standard deviation of grades per course

    Min/max grades per student

    Top 5 students by average

### Visualizations:

    Grade distribution histogram

    Grade intervals (0–5, 6–10, etc.) as bar chart

    Outputs: average_grades_chart.png

## 5.  Automation via GitHub Actions
    * Workflow: .github/workflows/run_analysis.yml

    * Triggers:

        - On push to main

        - Daily at 8:00 UTC (via cron)

    * Steps:

        - Clone repo

        - Set up Python & dependencies

        - Securely inject Snowflake credentials via GitHub Secrets

        - Run the analysis script

        - Upload generated files (e.g., PNG) as GitHub Artifacts


# 👨‍💻 Author
***Aymane RAMI***

**Data & Software Engineering Enthusiast**
