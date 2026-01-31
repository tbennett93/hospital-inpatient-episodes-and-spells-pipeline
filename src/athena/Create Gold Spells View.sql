create view hospital_data.vw_gold_spells as
with episode_level_data as (
SELECT
  spell_id,
  patient_id,
  ward ,
  consultant ,	
  discharge_dttm,
  case when discharge_dttm is not null then 'Y' else 'N' end as is_discharged,
  row_number() over (partition by spell_id order by episode_start_date desc)  as rn,
  first_value(episode_start_date) over (partition by spell_id order by episode_start_date) as admission_date
FROM
  hospital_data.silver_episodes
  
 )
 
 
select 
  spell_id,
  patient_id,
  ward as latest_ward_id,
  consultant ,	
  discharge_dttm,
  is_discharged,
  admission_date,
  date_diff('day', admission_date,  coalesce(cast(discharge_dttm as date), cast(now() as date)) ) as length_of_stay_days
from
    episode_level_data
where rn = 1