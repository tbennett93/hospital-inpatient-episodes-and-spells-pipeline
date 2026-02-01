create table hospital_data.silver_episodes
with (
	external_location = 's3://hospital-inpatients-pipeline/silver/episodes/',
	format = 'parquet'
)
as

select *
from hospital_data.vw_silver_episodes