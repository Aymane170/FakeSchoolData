{{ config(
    materialized='view'
) }}

with ranked_grades as (
    select
        fr.student_id,
        fr.course_id,
        fr.grade,
        rank() over (partition by fr.course_id order by fr.grade desc) as grade_rank
    from {{ ref('fact_results') }} as fr
)

select
    rg.student_id,
    s.firstname || ' ' || s.lastname as student_name,
    rg.course_id,
    c.nom as course_name,
    rg.grade
from ranked_grades as rg
join {{ ref('dim_students') }} as s
    on rg.student_id = s.id_student_hash
join {{ ref('dim_courses') }} as c
    on rg.course_id = c.id_course_hash
where rg.grade_rank = 1
