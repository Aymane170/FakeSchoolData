{{ config(
    materialized='view'
) }}

SELECT
    fr.course_id_hash,
    dc.nom AS course_name,
    COUNT(*) AS total_students,
    SUM(CASE WHEN fr.grade < 10 THEN 1 ELSE 0 END) AS failed_students,
    ROUND(100.0 * SUM(CASE WHEN fr.grade < 10 THEN 1 ELSE 0 END) / COUNT(*), 2) AS failure_rate
FROM {{ ref('fact_results') }} AS fr
JOIN {{ ref('dim_courses') }} AS dc
    ON fr.course_id_hash = dc.id_course_hash
GROUP BY fr.course_id_hash, dc.nom
ORDER BY failure_rate DESC
