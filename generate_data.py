import numpy as np
import pandas as pd
from faker import Faker
import random
from azure.storage.blob import BlobServiceClient
import os


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




# Variables Azure Storage
connect_str = "https://stafakeschooldata.blob.core.windows.net/data?sp=racwdl&st=2025-06-25T13:52:20Z&se=2025-07-25T21:52:20Z&spr=https&sv=2024-11-04&sr=c&sig=NQ3xHpX3p32b9c9w4GKaSKmA0kxEd8UBSJBow9HCMro%3D"  # depuis Azure Portal (Access Keys)
container_name = "source"  # ex: "csvfiles"

# Initialise le client BlobService
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Récupère le client du container
container_client = blob_service_client.get_container_client(container_name)

def upload_file_to_blob(local_file_path, blob_name):
    # Ouvre le fichier local en mode binaire
    with open(local_file_path, "rb") as data:
        container_client.upload_blob(name=blob_name, data=data, overwrite=True)
    print(f"✅ Upload réussi pour : {blob_name}")

# Exemple : uploader les 3 fichiers CSV générés
upload_file_to_blob("courses.csv", "courses.csv")
upload_file_to_blob("students.csv", "students.csv")
upload_file_to_blob("results.csv", "results.csv")