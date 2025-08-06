{{ config(
    materialized='incremental',
    unique_key='id_course_hash'
) }}

with raw_data as (
  select
    id,
    nom,
    annee_enseignement,
    nom_professeur,
    prenom_professeur
  from {{ source('raw', 'courses') }}
)

select
  id,
  nom,
  annee_enseignement,
  nom_professeur,
  prenom_professeur,  
  md5(concat(nom, cast(annee_enseignement as varchar))) as id_course_hash

from raw_data

{% if is_incremental() %}
  where id not in (select id from {{ this }})
{% endif %}
