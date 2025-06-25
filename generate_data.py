import numpy as np
import pandas as pd
from faker import Faker
import random


fake = Faker()
np.random.seed(42)
random.seed(42)

# Générer les cours
nb_cours = 10
cours = [{'id': i + 1, 'nom': fake.job()} for i in range(nb_cours)]
df_cours = pd.DataFrame(cours)
df_cours.to_csv('cours.csv', index=False)


# Générer les élèves
nb_eleves = 50
eleves = [{'id': i + 1, 'prenom': fake.first_name(), 'nom': fake.last_name()} for i in range(nb_eleves)]
df_eleves = pd.DataFrame(eleves)
df_eleves.to_csv('eleves.csv', index=False)


# Générer les résultats annuels
resultats = []
for eleve in eleves:
    for cours in df_cours['id']:
        note = round(np.random.normal(loc=12, scale=3), 2)  # moyenne autour de 12/20
        note = max(0, min(20, note))  
        resultats.append({
            'id_eleve': eleve['id'],
            'id_cours': cours,
            'note': note
        })

df_resultats = pd.DataFrame(resultats)
df_resultats.to_csv('resultats.csv', index=False)
