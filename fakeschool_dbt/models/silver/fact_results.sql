-- models/silver/fact_results.sql
/*
  Modèle fact_results : Résultats enrichis avec identifiants hashés
  Jointures avec dim_students et dim_courses pour récupérer les clés uniques
*/

{{ config(
    materialized='incremental',
    unique_key='student_id || course_id'
) }}

with results as (
    select *
    from {{ source('raw', 'results') }}
),

students as (
    select
        id as id_source_student,
        id_student_hash
    from {{ ref('dim_students') }}
),

courses as (
    select
        id as id_source_course,
        id_course_hash,
        annee_enseignement
    from {{ ref('dim_courses') }}

)

select
    s.id_student_hash as student_id_hash,
    c.id_course_hash as course_id_hash,
    c.annee_enseignement as annee,
    r.grade
from results r
left join students s on r.id_student = s.id_source_student
left join courses c on r.id_courses = c.id_source_course

