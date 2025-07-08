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
    "avg_grade_by_courses": "fakeschool_dbt/target/compiled/fakeschool_dbt/models/gold/avg_grade_by_course.sql",
    "avg_grade_by_students": "fakeschool_dbt/target/compiled/fakeschool_dbt/models/gold/avg_grade_by_student.sql",
    "courses_with_highest_failure_rate": "fakeschool_dbt/target/compiled/fakeschool_dbt/models/gold/courses_with_highest_failure_rate.sql",
    "top_students_per_courses": "fakeschool_dbt/target/compiled/fakeschool_dbt/models/gold/top_students_per_course.sql"
}

os.makedirs("charts", exist_ok=True)

for name, path in sql_files.items():
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

    # Plotting logic
    plt.figure(figsize=(10, 6))

    if name == "avg_grade_by_courses":
        # Grouped bar chart: average grade by course and year
        df["ANNEE_ENSEIGNEMENT"] = df["ANNEE_ENSEIGNEMENT"].astype(str)
        pivot_df = df.pivot(index="ANNEE_ENSEIGNEMENT", columns="COURSE_NAME", values="AVERAGE_GRADE")
        pivot_df.plot(kind="bar")
        plt.title("Average Grade by Course and Year")
        plt.ylabel("Average Grade")

    elif name == "avg_grade_by_students":
        # Top 10 students by average grade
        df_top = df.sort_values(by="AVERAGE_GRADE", ascending=False).head(10)
        df_top.plot(kind="bar", x="STUDENT_ID", y="AVERAGE_GRADE", legend=False, color="teal")
        plt.title("Top 10 Students by Average Grade")
        plt.ylabel("Average Grade")

    elif name == "courses_with_highest_failure_rate":
        # Top 10 failure rates
        df["FAILURE_RATE"] = pd.to_numeric(df["FAILURE_RATE"], errors="coerce")  # force en float
        df_sorted = df.sort_values(by="FAILURE_RATE", ascending=False).head(10)
        df_sorted.plot(kind="bar", x="COURSE_NAME", y="FAILURE_RATE", legend=False, color="tomato")

        print(df.dtypes)
        print(df.head())
        plt.title("Top 10 Courses with Highest Failure Rate")
        plt.ylabel("Failure Rate (%)")

    elif name == "top_students_per_courses":
        # One bar per course: best student and grade
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
