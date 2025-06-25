SELECT *
FROM {{ ref('average_grades') }}
ORDER BY average_grade DESC
LIMIT 3