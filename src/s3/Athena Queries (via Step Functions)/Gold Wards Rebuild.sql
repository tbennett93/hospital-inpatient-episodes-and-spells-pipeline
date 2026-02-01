CREATE TABLE hospital_data.gold_wards
WITH (
    external_location = 's3://hospital-inpatients-pipeline/gold/wards/',
    format = 'parquet'
)
AS
SELECT *
FROM hospital_data.vw_gold_wards
