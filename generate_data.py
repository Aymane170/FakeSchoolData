"""
Script de génération de données fictives pour un système scolaire
Ce script génère trois ensembles de données :
- Courses (cours) : Liste des cours avec leurs professeurs et années d'enseignement
- Students (étudiants) : Liste des étudiants avec leurs informations personnelles
- Results (résultats) : Notes des étudiants pour chaque cours

Les données sont générées de manière aléatoire mais cohérente grâce à l'utilisation
de seeds fixes pour la reproductibilité des résultats.
"""

import numpy as np  # Pour les calculs numériques et la génération de notes
import pandas as pd  # Pour la manipulation et l'export des données
from faker import Faker  # Pour la génération de données réalistes (noms, dates, etc.)
import random  # Pour les choix aléatoires
import os  # Pour la gestion des dossiers



"""
Configuration initiale du générateur de données
- Initialisation du Faker en français pour des données localisées
- Définition des seeds pour la reproductibilité
- Création du dossier de sortie
"""
fake = Faker('fr_FR')  # Initialisation du générateur de données en français
np.random.seed(42)     # Seed pour numpy - assure la reproductibilité des notes
random.seed(42)        # Seed pour les choix aléatoires
os.makedirs('seeds', exist_ok=True)  # Création du dossier de sortie si non existant

"""
Génération des données des cours
Cette section génère une liste de 10 cours avec :
- ID unique
- Nom du cours (basé sur un métier pour plus de réalisme)
- Année d'enseignement (2023 ou 2024)
- Nom et prénom du professeur
"""
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


"""
Génération des données des étudiants
Cette section crée 50 étudiants avec :
- ID unique
- Prénom et Nom
- Date de naissance (entre 18 et 22 ans)
- Date de dernière mise à jour des informations
Les données sont réalistes grâce à Faker et respectent une distribution d'âge cohérente
"""
number_of_students = 50  # Nombre total d'étudiants à générer
students = []  # Liste pour stocker les données des étudiants
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



"""
Génération des résultats académiques
Cette section génère les notes pour chaque combinaison étudiant-cours :
- Distribution normale centrée sur 12/20 (écart-type de 3)
- Notes bornées entre 0 et 20
- Génération systématique pour assurer que chaque étudiant a une note dans chaque cours
Les notes suivent une distribution réaliste avec une moyenne de classe de 12/20
"""
results = []  # Liste pour stocker toutes les notes
for student in students:  # Pour chaque étudiant
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
