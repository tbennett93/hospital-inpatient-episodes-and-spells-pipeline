import boto3


def execute_ctas(athena, sql_query, database):
    athena.start_query_execution(
        QueryString=sql_query,
        QueryExecutionContext={"Database": database},
        ResultConfiguration={
            "OutputLocation": "s3://hospital-inpatients-pipeline/athena-query-results"
        }
    )

def lambda_handler(event, context):

    expected_params = ['view_database','view_name','table_database','table_name','external_location','output_format']

    for param in expected_params:
        if param not in event:
            raise ValueError(f"Expected param {param}")

    athena = boto3.client('athena')

    view_database = event["view_database"]
    view_name = event["view_name"]
    table_database = event["table_database"]
    table_name = event["table_name"]
    external_location = event["external_location"]
    output_format = event["output_format"]

    

    SQL_QUERY = f"""
                create table {table_database}.{table_name}

                with (
                    external_location = '{external_location}',
                    format = '{output_format}'
                )
                as

                select *
                from {view_database}.{view_name}
                """


    execute_ctas(athena, SQL_QUERY, table_database)
        