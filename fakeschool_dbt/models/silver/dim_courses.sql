-- models/silver/dim_courses.sql
/*
  Modèle dim_courses : Dimension des cours nettoyée
  Source : raw.courses (seed table)
  Ajoute un identifiant unique hashé basé sur le nom du cours et l'année d'enseignement
  Conserve les informations sur le professeur
*/

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

  -- Création d'une clé de hachage unique pour chaque cours
  md5(concat(nom, cast(annee_enseignement as varchar))) as id_course_hash

from raw_data
