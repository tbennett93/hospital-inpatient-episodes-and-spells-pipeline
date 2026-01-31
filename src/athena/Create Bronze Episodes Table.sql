CREATE external TABLE hospital_data.bronze_episodes(
  `spell id` string, 
  `episode_id` string, 
  `patient_id` string, 
  `patient forename` string, 
  `patient surname` string, 
  `patient dob` string, 
  `episode start date` string, 
  `episode_end_date` string, 
  `ward` string, 
  `ward name` string, 
  `consultant` string, 
  `dicharge_dttm` string, 
  `last_updated_ts` string, 
  `ingest_dttm` timestamp, 
  `developer comment` string)
PARTITIONED BY ( 
  `snapshot_date` string)
STORED AS parquet
LOCATION
  's3://hospital-inpatients-pipeline/bronze/episodes/'
