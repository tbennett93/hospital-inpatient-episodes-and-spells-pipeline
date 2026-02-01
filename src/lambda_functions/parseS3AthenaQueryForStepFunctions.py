import boto3



def lambda_handler(event, context):

    s3 = boto3.client('s3')

    expected_params = ['bucket','key']

    for x in expected_params:
        if x not in event:
            raise ValueError(f"Missing expected parameter: {x}")

    file = s3.get_object(
        Bucket=event['bucket'], 
        Key=event['key']
    )

    sql = file["Body"].read().decode("utf-8")

    return{
        "sql":sql
    }