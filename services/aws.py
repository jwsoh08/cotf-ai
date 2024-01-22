import json
import boto3
from botocore.exceptions import ClientError


class SecretsManager:
    @staticmethod
    def get_secret(key):
        secret_name = "cotf/streamlit/test"
        region_name = "ap-southeast-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)

        except ClientError as e:
            raise e

        secrets = json.loads(get_secret_value_response["SecretString"])
        return secrets[key]
