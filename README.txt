Purpose
	Build a pipeline using source system inpatient episode/spell data to produce a spells and episodes fsct table with calculated measures appropriate dimensions

Use:
	-s3 for storage
	-boto3 for ingestion
	-athena for queries and defining table structures
	-medallion architecture
		-bronze
			-raw data
			-append only
			-CSV
			-daily snapshot of current system table, which presents 1 row per episode 
		-silver 
			-de-duplicated 
				-one row per episode representing latest episode data 
				-don't retain in-episode historical changes at this level - this will be done at gold level via SCD2
			-cleaned
				-standardise column name format	
				-trim empty characters
			-schema validation
			
		-gold - produce fact/dimension tables for episodes/spells. 
			-episodes
				-add latest_episode flag
				-add discharged flag
				-add episode number
				-represents latest version of an episode
			-spells 
				-one row per spell
				-derive spell LOS from first episode start date to last episode discharge
			-slowly changing dimensions (SCD2)
				-ward
				-patient
					-derive age at episode start
					-derive age at discharge
				-consultant

-Patients are admitted
-Their episode can change while active
-Once discharged, records become immutable

