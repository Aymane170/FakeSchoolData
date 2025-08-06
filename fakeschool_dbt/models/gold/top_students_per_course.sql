{{ config(
    materialized='view'
) }}

WITH ranked_grades AS (
    SELECT
        fr.student_id_hash,
        fr.course_id_hash,
        fr.grade,
        RANK() OVER (PARTITION BY fr.course_id_hash ORDER BY fr.grade DESC) as grade_rank
    FROM {{ ref('fact_results') }} as fr
)

SELECT
    rg.student_id_hash,
    rg.course_id_hash,
    c.nom as course_name,
    rg.grade
FROM ranked_grades as rg
JOIN {{ ref('dim_courses') }} as c
    ON rg.course_id_hash = c.id_course_hash
WHERE rg.grade_rank = 1
