    {{ config(
        materialized='view'
    ) }}

    select
        fr.course_id_hash,
        dc.nom as course_name,
        count(*) as total_students,
        sum(case when fr.grade < 10 then 1 else 0 end) as failed_students,
        round(100.0 * sum(case when fr.grade < 10 then 1 else 0 end) / count(*), 2) as failure_rate
    from {{ ref('fact_results') }} as fr
    join {{ ref('dim_courses') }} as dc
        on fr.course_id_hash = dc.id_course_hash
    group by fr.course_id_hash, dc.nom
    order by failure_rate desc
