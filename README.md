![CI](https://github.com/Aymane170/FakeSchoolData/actions/workflows/run_analysis.yml/badge.svg)


# **FakeSchoolData**

A fully automated data pipeline that simulates school data, loads it into Snowflake, transforms it using dbt (Silver & Gold models), and generates visual insights with Python — all scheduled daily via GitHub Actions.



## 🎯 **Project Overview**

FakeSchoolData is a personal data engineering project designed to simulate, transform, and analyze fictional academic data. It covers the entire data lifecycle: data generation, ingestion, transformation, visualization, and automation.

This project demonstrates the use of a modern data stack in a complete end-to-end scenario.



## 🧰 **Tech Stack**

- **Languages**: Python 3.10, SQL  
- **Python Libraries**: `pandas`, `numpy`, `matplotlib`, `faker`, `snowflake-connector-python`  
- **Data Warehouse**: Snowflake  
- **Transformation Tool**: dbt (Data Build Tool)  
- **CI/CD**: GitHub Actions  
- **Visualization & Automation**: Python + matplotlib  
- **Version Control**: Git



## 📁 **Repository Structure**


        FakeSchoolData/
        ├── .github/
        │   └── workflows/
        │       └── run_analysis.yml          # GitHub Actions CI/CD workflow (automated analysis)
        ├── generate_data.py                  # Script to generate fake school data
        ├── generate_gold_graphs.py           # Script to generate charts from Gold dbt models
        ├── charts/                          # Folder for auto-generated PNG charts
        ├── fakeschool_dbt/                  # dbt project for data transformations
        │   ├── dbt_project.yml              # dbt project configuration file
        │   ├── seeds/                      
        │   │   ├── students.csv             # Seed data: students
        │   │   ├── courses.csv              # Seed data: courses
        │   │   └── results.csv              # Seed data: student results
        │   └── models/
        │       ├── silver/                  # Silver layer models (cleaned/raw data)
        │       │   ├── dim_courses.sql      # Dimension table for courses
        │       │   ├── dim_students.sql     # Dimension table for students
        │       │   ├── fact_results.sql     # Fact table for results/grades
        │       │   ├── results_cleaned.sql  # Cleaned results data
        │       │   └── schema.yml           # Documentation & tests for silver models
        │       └── gold/                    # Gold layer models (aggregated & analytic)
        │           ├── avg_grade_per_course.sql               # Average grades by course
        │           ├── avg_grade_per_students.sql             # Average grades by student
        │           ├── top_student_per_course.sql             # Top student per course
        │           └── course_with_highest_failure_rate.sql  # Courses with highest failure rates
        ├── .gitignore                      # Git ignore rules



## 🔁 **Workflow Summary**

### 1. **Data Generation – `generate_data.py`**

This script uses Faker, Numpy, and Pandas to create realistic datasets:

- **Students**: 100 (ID, first name, last name)  
- **Courses**: 10 (ID, name)  
- **Results**: Random grades (0 to 20) for each student-course pair

**Output**:  
CSV files saved to `fakeschool_dbt/seeds/`  
(`students.csv`, `courses.csv`, `results.csv`)



### 2. **Load into Snowflake**

- Connects to Snowflake using `snowflake-connector-python`  
- Loads CSV data via `dbt seed`  
- Creates RAW tables (staging layer)  
- Prepares for dbt transformation



### 3. **Data Transformation with dbt**

The `fakeschool_dbt` project is structured into two layers:

#### 🧪 **Silver (Cleaning & Structuring)**

- `dim_students.sql`: Student dimension table  
- `dim_courses.sql`: Course dimension table  
- `fact_results.sql`: Results fact table  
- `results_cleaned.sql`: Initial data cleanup  
- `schema.yml`: Model documentation and automated tests

#### 📊 **Gold (Business-Ready Analytics)**

- `avg_grade_per_course.sql`: Average grade by course  
- `avg_grade_per_students.sql`: Average grade by student  
- `top_student_per_course.sql`: Top student per course  
- `course_with_highest_failure_rate.sql`: Courses with the highest failure rates



### 4. **Visualization – `generate_gold_graphs.py`**

This script queries the Gold models from Snowflake and generates charts using pandas and matplotlib:

- Grade distributions (histograms)  
- Averages per course/student  
- Failure rates  
- Top performers

**Charts are saved to the `charts/` directory.**



### 5. **Automation – GitHub Actions**

- **Workflow file**: `.github/workflows/run_analysis.yml`  
- **Triggers**:
  - On every push to `main`
  - Daily at `08:00 UTC` via cron

**Steps executed automatically:**

1. Install Python and dependencies  
2. Inject Snowflake credentials via GitHub Secrets  
3. Run `generate_gold_graphs.py`  
4. Generate updated charts  
5. Store charts in `charts/` or as GitHub Artifacts



## 📊 **Sample Charts**

Charts are refreshed daily and may include:

- Grade distribution per course  
- Top students by average  
- Courses with highest failure rates  
- Average scores by student



## 👨‍💻 **Author**

**Aymane RAMI**  
*Data & Software Engineering Enthusiast*
