{{ config(
    materialized='view'
) }}

WITH ranked_grades AS (
    SELECT
        fr.student_id,
        fr.course_id,
        fr.grade,
        RANK() OVER (PARTITION BY fr.course_id ORDER BY fr.grade DESC) as grade_rank
    FROM {{ ref('fact_results') }} as fr
)

SELECT
    rg.student_id,
    rg.course_id,
    c.nom as course_name,
    rg.grade
FROM ranked_grades as rg
JOIN {{ ref('dim_courses') }} as c
    ON rg.course_id = c.id_course
WHERE rg.grade_rank = 1
