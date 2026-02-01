create table hospital_data.gold_patients
with (
	external_location = 's3://hospital-inpatients-pipeline/gold/patients/',
	format = 'parquet'
)
as

select *
from hospital_data.vw_gold_patients