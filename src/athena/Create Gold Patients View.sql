create view hospital_data.vw_gold_patients as 

select distinct patient_id, patient_forename, patient_surname, patient_dob
from silver_episodes
  
  