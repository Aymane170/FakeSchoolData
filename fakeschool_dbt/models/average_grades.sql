SELECT
    id_student,
    AVG(grade) AS average_grade
FROM {{ source('raw', 'Results') }}
GROUP BY id_student