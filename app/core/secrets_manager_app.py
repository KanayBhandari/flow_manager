import boto3
import json
import os
from functools import lru_cache


@lru_cache()
def get_db_credentials():
    client = boto3.client(
        "secretsmanager",
        region_name=os.environ["AWS_REGION"]
    )

    response = client.get_secret_value(
        SecretId=os.environ["DB_SECRET_NAME"]
    )

    secret = json.loads(response["SecretString"])

    return secret["username"], secret["password"]

# print(get_db_credentials())
