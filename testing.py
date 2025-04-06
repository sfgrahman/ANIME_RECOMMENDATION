import boto3
from config.paths_config import * 

s3_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin"
)
bucket_name="anime-recommendation"
# response = s3_client.list_objects_v2(Bucket=bucket_name)
# if "Contents" in response:
#     for obj in response["Contents"]:
#         print(obj["Key"])  # Prints each file name (object key)
# else:
#     print("Bucket is empty.")


                
s3_client.download_file(bucket_name, "anime.csv", "anime.csv",)