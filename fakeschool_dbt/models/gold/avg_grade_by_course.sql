{{ config(
    materialized='view'
) }}

SELECT
  c.nom AS course_name,
  c.annee_enseignement,
  ROUND(AVG(r.grade), 2) AS average_grade
FROM {{ ref('fact_results') }} r
JOIN {{ ref('dim_courses') }} c ON r.course_id = c.id_course
GROUP BY c.nom, c.annee_enseignement
ORDER BY average_grade DESC
