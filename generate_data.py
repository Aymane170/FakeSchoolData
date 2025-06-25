import numpy as np
import pandas as pd
from faker import Faker
import random


fake = Faker('fr_FR') 
np.random.seed(42)
random.seed(42)

# Générer les cours
number_of_courses = 10
courses = [{'id': i + 1, 'nom': fake.job()} for i in range(number_of_courses)]
df_courses = pd.DataFrame(courses)
df_courses.to_csv('courses.csv', index=False, encoding='utf-8-sig')


# Générer les élèves
number_of_students = 50
students = [{'id': i + 1, 'firstname': fake.first_name(), 'lastname': fake.last_name()} for i in range(number_of_students)]
df_students = pd.DataFrame(students)
df_students.to_csv('students.csv', index=False, encoding='utf-8-sig')


# Générer les résultats annuels
results = []
for student in students:
    for courses in df_courses['id']:
        grade = round(np.random.normal(loc=12, scale=3), 2)  # moyenne autour de 12/20
        grade = max(0, min(20, grade))  
        results.append({
            'id_student': student['id'],
            'id_courses': courses,
            'grade': grade
        })

df_results = pd.DataFrame(results)
df_results.to_csv('results.csv', index=False, encoding='utf-8-sig')
