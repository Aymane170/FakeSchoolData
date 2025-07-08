import os
import pandas as pd
import matplotlib.pyplot as plt
import snowflake.connector

print("🔗 Connexion à Snowflake...")

conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    schema=os.getenv('SNOWFLAKE_SCHEMA')
)

cursor = conn.cursor()

sql_files = {
    "avg_grade_by_courses": "fakeschool_dbt/models/gold/avg_grade_by_course.sql",
    "avg_grade_by_students": "fakeschool_dbt/models/gold/avg_grade_by_student.sql",
    "courses_with_highest_failure_rate": "fakeschool_dbt/models/gold/courses_with_highest_failure_rate.sql",
    "top_students_per_courses": "fakeschool_dbt/models/gold/top_students_per_course.sql"
}

os.makedirs("charts", exist_ok=True)

for name, path in sql_files.items():
    print(f"📄 Exécution de {path}")
    with open(path, "r") as f:
        query = f.read()
        cursor.execute(query)
        df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])

    if df.empty:
        print(f"⚠️ Résultat vide pour {name}")
        continue

    # Graphique simple selon le cas
    plt.figure(figsize=(8,5))
    
    if "GRADE" in df.columns or "AVG_GRADE" in df.columns:
        x_col = df.columns[0]
        y_col = df.columns[1]
        df.plot(kind="bar", x=x_col, y=y_col, legend=False, color="skyblue")
        plt.title(name.replace("_", " ").title())
        plt.ylabel(y_col)
    else:
        df.plot(kind="bar")
        plt.title(name.replace("_", " ").title())

    plt.tight_layout()
    output_path = f"charts/{name}.png"
    plt.savefig(output_path)
    print(f"✅ Graphique sauvegardé dans {output_path}")
    plt.close()

cursor.close()
conn.close()
print("🎉 Tous les graphiques générés avec succès.")
