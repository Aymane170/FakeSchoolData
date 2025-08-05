-- models/silver/results_cleaned.sql
/*
  Modèle results_cleaned : Résultats enrichis avec identifiants hashés
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
        id as student_id,
        id_student_hash
    from {{ ref('dim_students') }}
),

courses as (
    select
        id as course_id,
        id_course_hash,
        annee_enseignement
    from {{ ref('dim_courses') }}
)

select
    s.id_student_hash as student_id,
    c.id_course_hash as course_id,
    c.annee_enseignement as annee,
    r.grade
from results r
left join students s on r.id_student = s.student_id
left join courses c on r.id_courses = c.course_id
