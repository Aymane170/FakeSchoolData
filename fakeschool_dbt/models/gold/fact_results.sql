-- models/gold/fact_results.sql
/*
  Table de faits finale des résultats :
  Combine les résultats, les étudiants et les cours
*/

{{ config(
    materialized='incremental',
    unique_key='student_id || course_id'
) }}

with results as (
    select *
    from {{ ref('results_cleaned') }}
),

students as (
    select
        id_student_hash,
        firstname,
        lastname,
        date_naissance,
        matricule
    from {{ ref('dim_students') }}
),

courses as (
    select
        id_course_hash,
        nom as nom_cours,
        annee_enseignement,
        nom_professeur,
        prenom_professeur
    from {{ ref('dim_courses') }}
)

select
    r.student_id,
    s.firstname,
    s.lastname,
    s.date_naissance,
    s.matricule,

    r.course_id,
    c.nom_cours,
    c.annee_enseignement,
    c.nom_professeur,
    c.prenom_professeur,

    r.grade
from results r
left join students s on r.student_id = s.id_student_hash
left join courses c on r.course_id = c.id_course_hash
