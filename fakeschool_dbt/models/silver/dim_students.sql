{{ config(
    materialized='incremental',
    unique_key='id'
) }}

with latest as (
    select max(updated_at) as max_updated_at from {{ source('raw', 'students') }}
),

raw_data as (
    select *
    from {{ source('raw', 'students') }}
    {% if is_incremental() %}
        where updated_at > (select max_updated_at from latest)
    {% endif %}
)

select
    id,
    firstname,
    lastname,
    date_naissance,
    md5(concat(firstname, lastname, date_naissance)) as matricule,
    updated_at
from raw_data
