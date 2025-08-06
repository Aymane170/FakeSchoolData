{{ config(
    materialized='incremental',
    unique_key='student_id_hash || course_id_hash'
) }}

with results as (
    select
        id_student,
        id_courses,
        grade
    from {{ source('raw', 'results') }}
),

students as (
    select
        id
    from {{ ref('dim_students') }}
),

courses as (
    select
        id,
        nom,
        annee_enseignement
    from {{ ref('dim_courses') }}
)

select
    md5(cast(r.id_student as string)) as student_id_hash,
    md5(concat(c.nom, cast(c.annee_enseignement as varchar))) as course_id_hash,
    c.annee_enseignement as annee,
    r.grade
from results r
left join students s on r.id_student = s.id
left join courses c on r.id_courses = c.id
