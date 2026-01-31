WIP

Purpose
	Using AWS services, build a pipeline using source system inpatient episode/spell data to produce a spells and episodes fsct table with calculated measures and appropriately modelled dimensions

Use:
	-s3 for storage
	-boto3 for ingestion
	-athena for queries and defining table structures
	-medallion architecture
		-bronze
			-raw data
			-append only
			-simple conversion from csv to parquet
			-daily snapshot of current system table, which presents 1 row per episode 
			-source system to push daily
		-silver 
			-de-duplicated 
				-one row per episode representing latest episode data 
				-don't retain in-episode historical changes at this level - this will be done at gold level via SCD2
			-cleaned
				-standardise column name format	
				-trim empty characters
			-schema validation
				-date conversion - fail hard on unexpected values
			-table rebuilt daily with new snapshot files
				-the size of the table doesn't justify incremental loads			
			-trigger
				-event bridge on a set schedule 8am
		
	
	
		-gold - produce fact/dimension tables for episodes/spells. 
			-episodes
				-add latest_episode in_spell flag x
				-add discharged flag x
				-add episode number x
				-represents latest version of an episode x
			-spells 
				-one row per spell
				-derive spell LOS from first episode start date to last episode discharge
			-dimensions (SCD1 - keep most recent
				-ward
				-patient
					-derive age at episode start
					-derive age at discharge
				-consultant

-Patients are admitted
-Their episode can change while active
-Once discharged, records become immutable


TODO
	-async waits
	-alert on empty source tables
	-delete s3 data to continue even if no data found (don't fail)
	-report failures from athena in step funcs
	-schedule gold rebuild or orchestrate to begin after silver
	


talk about
	-why used athena
	-why used a view
	-why drop and rebuild
	-why not SCD2
	-why not a dimension for consultant
		-source doesn't have any other consultant info, it would be a single column consultant 
	-creating a relational schema in gold
		-normalising the fields somewhat - separating out to dimensions from a flat table
		
	-modularising lambda functions to be executed in step functions
	-how the SCD1s can be created just from silver as silver is most recent episode

dependencies:
	-pandas (import)