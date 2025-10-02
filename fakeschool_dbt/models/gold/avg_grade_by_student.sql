{{ config(
    materialized='view'
) }}

SELECT
  r.student_id_hash,
  ROUND(AVG(r.grade), 2) AS average_grade


FROM {{ ref('fact_results') }} r


GROUP BY r.student_id_hash
ORDER BY average_grade DESC
/* Having */