{{ config(
    materialized='view'
) }}

SELECT
  r.student_id,
  ROUND(AVG(r.grade), 2) AS average_grade
FROM {{ ref('fact_results') }} r
GROUP BY r.student_id
ORDER BY average_grade DESC
