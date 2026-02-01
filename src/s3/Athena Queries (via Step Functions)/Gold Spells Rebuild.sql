create table hospital_data.gold_spells
with (
	external_location = 's3://hospital-inpatients-pipeline/gold/spells/',
	format = 'parquet'
)
as

select *
from hospital_data.vw_gold_spells