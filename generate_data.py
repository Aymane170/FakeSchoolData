"""
Script de génération incrémentale de données fictives pour un système scolaire
Ajoute de nouveaux cours, étudiants et résultats à chaque exécution sans écraser les fichiers existants.
"""

from datetime import datetime
import numpy as np
import pandas as pd
from faker import Faker
import random
import os

# Configuration des chemins
COURSES_PATH = 'fakeschool_dbt/seeds/courses.csv'
STUDENTS_PATH = 'fakeschool_dbt/seeds/students.csv'
RESULTS_PATH = 'fakeschool_dbt/seeds/results.csv'
os.makedirs('fakeschool_dbt/seeds', exist_ok=True)

seed = int(datetime.now().timestamp())
print(f"Seed utilisée : {seed}")
np.random.seed(seed)
random.seed(seed)
fake = Faker('fr_FR')
Faker.seed(seed)

# Chargement ou initialisation des données existantes
if os.path.exists(COURSES_PATH):
    df_courses = pd.read_csv(COURSES_PATH)
    last_course_id = df_courses['id'].max()
else:
    df_courses = pd.DataFrame(columns=['id', 'nom', 'annee_enseignement', 'nom_professeur', 'prenom_professeur'])
    last_course_id = 0

if os.path.exists(STUDENTS_PATH):
    df_students = pd.read_csv(STUDENTS_PATH)
    last_student_id = df_students['id'].max()
else:
    df_students = pd.DataFrame(columns=['id', 'firstname', 'lastname', 'date_naissance', 'updated_at'])
    last_student_id = 0

if os.path.exists(RESULTS_PATH):
    df_results = pd.read_csv(RESULTS_PATH)
else:
    df_results = pd.DataFrame(columns=['id_student', 'id_courses', 'grade'])

# Génération de 10 nouveaux cours
new_courses = []
for i in range(10):
    new_courses.append({
        'id': last_course_id + i + 1,
        'nom': fake.job(),
        'annee_enseignement': random.choice([2023, 2024]),
        'nom_professeur': fake.last_name(),
        'prenom_professeur': fake.first_name()
    })
df_new_courses = pd.DataFrame(new_courses)

# Génération de 50 nouveaux étudiants
new_students = []
for i in range(50):
    new_students.append({
        'id': last_student_id + i + 1,
        'firstname': fake.first_name(),
        'lastname': fake.last_name(),
        'date_naissance': fake.date_of_birth(minimum_age=18, maximum_age=22).strftime('%Y-%m-%d'),
        'updated_at': fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S')
    })
df_new_students = pd.DataFrame(new_students)

# Mise à jour des DataFrames cumulés
df_courses = pd.concat([df_courses, df_new_courses], ignore_index=True)
df_students = pd.concat([df_students, df_new_students], ignore_index=True)

# Génération des résultats pour les NOUVEAUX étudiants dans TOUS les cours 
results = []
for student_id in df_new_students['id']:
    for course_id in df_courses['id']:
        grade = round(np.random.normal(loc=12, scale=3), 2)
        grade = max(0, min(20, grade))
        results.append({
            'id_student': student_id,
            'id_courses': course_id,
            'grade': grade
        })
df_new_results = pd.DataFrame(results)
df_results = pd.concat([df_results, df_new_results], ignore_index=True)

# Sauvegarde des fichiers
df_courses.to_csv(COURSES_PATH, index=False, encoding='utf-8')
df_students.to_csv(STUDENTS_PATH, index=False, encoding='utf-8')
df_results.to_csv(RESULTS_PATH, index=False, encoding='utf-8')

print("✅ Données enrichies avec succès.")
print(f"🎓 Total étudiants : {len(df_students)}")
print(f"📚 Total cours : {len(df_courses)}")
print(f"📝 Total résultats : {len(df_results)}")
 