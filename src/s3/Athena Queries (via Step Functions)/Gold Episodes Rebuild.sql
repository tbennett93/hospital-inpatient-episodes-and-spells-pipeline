create table hospital_data.gold_episodes
with (
	external_location = 's3://hospital-inpatients-pipeline/gold/episodes/',
	format = 'parquet'
)
as

select *
from hospital_data.vw_gold_episodes