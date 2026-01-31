import boto3



def remove_table_files(s3, bucket:str, prefix: str):
    files_to_delete = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    files_to_delete = files_to_delete["Contents"]
    for file in files_to_delete:
        if file["Key"] == prefix:
            continue    
        s3.delete_object(
            Bucket=bucket,
            Key = file["Key"]
        )


def lambda_handler(event, context):

    expected_params = ['bucket','prefix']

    for param in expected_params:
        if param not in event:
            raise ValueError(f"Didnt receive expected param {param}")

    s3 = boto3.client('s3')
    bucket = event["bucket"]
    prefix = event["prefix"]

    remove_table_files(s3, bucket, prefix)