"""
Script de génération de graphiques à partir des modèles dbt Gold
Ce script:
1. Se connecte à Snowflake pour récupérer les données analysées
2. Exécute les requêtes SQL compilées par dbt
3. Génère des visualisations pour chaque analyse
4. Sauvegarde les graphiques au format PNG

Les graphiques générés incluent:
- Moyennes par cours et par année
- Top 10 des étudiants
- Taux d'échec par cours
- Meilleurs étudiants par cours
"""

import os  # Pour la gestion des fichiers et dossiers
import pandas as pd  # Pour la manipulation des données
import matplotlib.pyplot as plt  # Pour la création des graphiques
import snowflake.connector  # Pour la connexion à la base de données Snowflake

print("🔗 Connexion à Snowflake...")

"""
Configuration de la connexion à Snowflake
Les credentials sont récupérés depuis les variables d'environnement
pour des raisons de sécurité et de portabilité
"""
conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    schema=os.getenv('SNOWFLAKE_SCHEMA')
)

cursor = conn.cursor()

"""
Définition des chemins vers les fichiers SQL compilés par dbt
Ces fichiers contiennent les requêtes optimisées pour chaque analyse
"""
sql_files = {
    "avg_grade_by_courses": "fakeschool_dbt/target/compiled/fakeschool_dbt/models/gold/avg_grade_by_course.sql",
    "avg_grade_by_students": "fakeschool_dbt/target/compiled/fakeschool_dbt/models/gold/avg_grade_by_student.sql",
    "courses_with_highest_failure_rate": "fakeschool_dbt/target/compiled/fakeschool_dbt/models/gold/courses_with_highest_failure_rate.sql",
    "top_students_per_courses": "fakeschool_dbt/target/compiled/fakeschool_dbt/models/gold/top_students_per_course.sql"
}

os.makedirs("charts", exist_ok=True)

"""
Boucle principale de génération des graphiques
Pour chaque fichier SQL:
1. Vérifie l'existence du fichier
2. Lit et exécute la requête
3. Convertit les résultats en DataFrame
4. Génère le graphique approprié
5. Sauvegarde le graphique en PNG
"""
for name, path in sql_files.items():
    # Vérification de l'existence du fichier SQL
    if not os.path.isfile(path):
        print(f"❌ Le fichier {path} n'existe pas. Passage à la suite.")
        continue

    print(f"📄 Exécution de {path}")
    with open(path, "r") as f:
        query = f.read()

    print("Requête SQL exécutée :")
    print(query[:200] + "..." if len(query) > 200 else query)

    cursor.execute(query)
    df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])

    if df.empty:
        print(f"⚠️ Résultat vide pour {name}")
        continue

    """
    Logique de génération des graphiques
    Chaque type d'analyse a son propre format de visualisation adapté :
    - avg_grade_by_courses : Graphique en barres groupées par année
    - avg_grade_by_students : Top 10 des moyennes étudiants
    - courses_with_highest_failure_rate : Taux d'échec par cours
    - top_students_per_courses : Meilleur étudiant par cours
    """
    plt.figure(figsize=(10, 6))

    if name == "avg_grade_by_courses":
        """
        Graphique des moyennes par cours et par année
        - Conversion de l'année en string pour le groupement
        - Création d'un tableau croisé pour les barres groupées
        - Affichage des moyennes par cours, groupées par année
        """
        df["ANNEE_ENSEIGNEMENT"] = df["ANNEE_ENSEIGNEMENT"].astype(str)
        pivot_df = df.pivot(index="ANNEE_ENSEIGNEMENT", columns="COURSE_NAME", values="AVERAGE_GRADE")
        pivot_df.plot(kind="bar")
        plt.title("Average Grade by Course and Year")
        plt.ylabel("Average Grade")

    elif name == "avg_grade_by_students":
        """
        Graphique des 10 meilleurs étudiants
        - Tri des moyennes par ordre décroissant
        - Sélection des 10 premiers
        - Graphique en barres avec couleur personnalisée
        """
        df_top = df.sort_values(by="AVERAGE_GRADE", ascending=False).head(10)
        df_top.plot(kind="bar", x="STUDENT_ID", y="AVERAGE_GRADE", legend=False, color="teal")
        plt.title("Top 10 Students by Average Grade")
        plt.ylabel("Average Grade")

    elif name == "courses_with_highest_failure_rate":
        """
        Graphique des cours avec le plus haut taux d'échec
        - Conversion du taux d'échec en nombre
        - Tri par taux d'échec décroissant
        - Graphique en barres rouge pour signaler les échecs
        """
        df["FAILURE_RATE"] = pd.to_numeric(df["FAILURE_RATE"], errors="coerce")  # force en float
        df_sorted = df.sort_values(by="FAILURE_RATE", ascending=False).head(10)
        df_sorted.plot(kind="bar", x="COURSE_NAME", y="FAILURE_RATE", legend=False, color="tomato")

        print(df.dtypes)
        print(df.head())
        plt.title("Top 10 Courses with Highest Failure Rate")
        plt.ylabel("Failure Rate (%)")

    elif name == "top_students_per_courses":
        """
        Graphique des meilleurs étudiants par cours
        - Création d'une étiquette combinant cours et ID étudiant
        - Un graphique en barres dorées pour les "meilleurs"
        - Affichage de la note du meilleur étudiant pour chaque cours
        """
        df["LABEL"] = df["COURSE_NAME"] + " (" + df["STUDENT_ID"].astype(str) + ")"
        df.plot(kind="bar", x="LABEL", y="GRADE", legend=False, color="goldenrod")
        plt.title("Top Student per Course")
        plt.ylabel("Grade")

    plt.tight_layout()
    output_path = f"charts/{name}.png"
    plt.savefig(output_path)
    print(f"✅ Graphique sauvegardé dans {output_path}")
    plt.close()

cursor.close()
conn.close()
print("🎉 Tous les graphiques générés avec succès.")
