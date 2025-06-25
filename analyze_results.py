import pandas as pd
import matplotlib.pyplot as plt
import snowflake.connector
import os

# Connexion à Snowflake (à adapter avec tes infos)
conn = snowflake.connector.connect(
    user='AYMANE17',
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account='LKJZRTO-NM04387',
    warehouse='COMPUTE_WH',
    database='FakeSchool',
    schema='RAW'
)

# Chargement des données dans DataFrame
query = """
SELECT 
    r.ID_STUDENT,
    s.FIRSTNAME || ' ' || s.LASTNAME AS student_name,
    r.ID_COURSES,
    c.NAME AS course_name,
    r.GRADE
FROM 
    RESULTS r
JOIN 
    STUDENTS s ON r.ID_STUDENT = s.ID
JOIN
    COURSES c ON r.ID_COURSES = c.ID
"""

df = pd.read_sql(query, conn)

print(df.columns)  

# Moyenne, médiane et écart-type des notes par cours
stats_by_course = df.groupby('ID_COURSES')['GRADE'].agg(['mean', 'median', 'std']).reset_index()
print("Stats par cours :\n", stats_by_course)

# Distribution des notes (histogramme)
plt.figure(figsize=(8,5))
plt.hist(df['GRADE'], bins=10, color='skyblue', edgecolor='black')
plt.title('Distribution des notes')
plt.xlabel('Note')
plt.ylabel('Nombre d\'étudiants')
plt.show()

# Nombre d’étudiants par cours
students_per_course = df.groupby('ID_COURSES')['ID_STUDENT'].nunique().reset_index(name='nb_students')
print("Nombre d'étudiants par cours :\n", students_per_course)

# Notes min et max par étudiant
min_max_by_student = df.groupby('ID_STUDENT')['GRADE'].agg(['min', 'max']).reset_index()
print("Notes min et max par étudiant :\n", min_max_by_student)

# Top 5 étudiants par moyenne
avg_by_student = df.groupby('ID_STUDENT')['GRADE'].mean().reset_index()
top_5_students = avg_by_student.sort_values(by='GRADE', ascending=False).head(5)
print("Top 5 étudiants par moyenne :\n", top_5_students)

# Répartition des notes par tranche
bins = [0, 5, 10, 15, 20]
labels = ['0-5', '6-10', '11-15', '16-20']
df['grade_range'] = pd.cut(df['GRADE'], bins=bins, labels=labels, right=True)
grade_distribution = df['grade_range'].value_counts().sort_index()
print("Répartition des notes par tranche :\n", grade_distribution)

grade_distribution.plot(kind='bar', color='orange')
plt.title('Répartition des notes par tranche')
plt.xlabel('Tranche de notes')
plt.ylabel('Nombre d\'étudiants')
plt.show()

conn.close()
