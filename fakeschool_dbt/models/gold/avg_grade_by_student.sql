{{ config(
    materialized='view'
) }}

SELECT
  s.firstname,
  s.lastname,
  ROUND(AVG(r.grade), 2) AS average_grade
FROM raw.fact_results r
JOIN raw.dim_students s ON r.student_id = s.id_student_hash
GROUP BY s.firstname, s.lastname
ORDER BY average_grade DESC
