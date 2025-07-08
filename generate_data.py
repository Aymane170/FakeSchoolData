import numpy as np
import pandas as pd
from faker import Faker
import random
import os 



fake = Faker('fr_FR') 
np.random.seed(42)
random.seed(42)
os.makedirs('seeds', exist_ok=True)


# Générer les cours avec année d'enseignement
number_of_courses = 10
courses = []
for i in range(number_of_courses):
    annee_enseignement = random.choice([2023, 2024])
    courses.append({
        'id': i + 1,
        'nom': fake.job(),
        'annee_enseignement': annee_enseignement,
        'nom_professeur': fake.last_name(),
        'prenom_professeur': fake.first_name()
    })
df_courses = pd.DataFrame(courses)
df_courses.to_csv('fakeschool_dbt/seeds/courses.csv', index=False, encoding='utf-8')


# Générer les élèves avec date de naissance
number_of_students = 50
students = []
for i in range(number_of_students):
    date_naissance = fake.date_of_birth(minimum_age=18, maximum_age=22).strftime('%Y-%m-%d')
    students.append({
        'id': i + 1,
        'firstname': fake.first_name(),
        'lastname': fake.last_name(),
        'date_naissance': date_naissance,
        'updated_at': fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S')

    })
df_students = pd.DataFrame(students)
df_students.to_csv('fakeschool_dbt/seeds/students.csv', index=False, encoding='utf-8')



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
df_results.to_csv('fakeschool_dbt/seeds/results.csv', index=False, encoding='utf-8')
