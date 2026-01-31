create view hospital_data.vw_gold_wards
as
select distinct ward as ward_id, ward_name
from silver_episodes
  
  