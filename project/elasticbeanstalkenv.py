import boto3
import json

# Create an Elastic Beanstalk client
eb_client = boto3.client("elasticbeanstalk", region_name="us-west-1")
s3_client = boto3.client('s3')

def SetEnv():
    environment_name = "Test-Ang-env"
    ApplicationName="Test-Ang"
    variables = []
    with open(".env", "r") as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespaces and newlines
            if line and not line.startswith("#"):  # Ignore empty lines and comments
                key, value = line.split("=", 1)
                variables.append(
                    {
                        "Namespace": "aws:elasticbeanstalk:application:environment",
                        "OptionName": key,
                        "Value": value,
                    },
                )
    # Update the environment variables
    response = eb_client.update_environment(
        ApplicationName=ApplicationName,
        EnvironmentName=environment_name,
        OptionSettings=variables,
    )
    print("Environment variables updated successfully.")

def SetBucketSettings(bucket_name):
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": [
                    f"arn:aws:s3:::{bucket_name}",
                    f"arn:aws:s3:::{bucket_name}/*"
                ]
            }
        ]
    }
    bucket_policy_str = json.dumps(bucket_policy)
    s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_str)
    print(f"Bucket policy set for {bucket_name}.")

    # Define your CORS configuration as a list of dictionaries
    cors_configuration = {
        'CORSRules': [{
            "AllowedHeaders": [
                "*"
            ],
            "AllowedMethods": [
                "GET",
                "PUT",
                "POST",
                "DELETE"
            ],
            "AllowedOrigins": [
                "*"
            ],
            "ExposeHeaders": []
        }]
    }
    s3_client.put_bucket_cors(Bucket=bucket_name,CORSConfiguration=cors_configuration)
    print(f"Bucket CORs set for {bucket_name}.")