from common.aws_client import AWSClient
from dotenv import dotenv_values
from common.logger import logger
from os import path, makedirs

env = dotenv_values()


def download_s3_data_from_bucket(output_path, folder_name: str = "queplan_insurance"):
    """
    Downloads data from an S3 bucket to a specified local directory.

    This function connects to an AWS S3 bucket using credentials and configuration
    provided by the AWSClient. It lists the objects in the specified folder within 
    the S3 bucket and downloads each object to a local directory.

    Args
        output_path: The local directory where files will be downloaded.
        folder_name: The folder within the S3 bucket from which to download files. 
        Defaults to "queplan_insurance".

    Returns
        None
    """
    s3_client = AWSClient().get_s3_client()
    bucket_name = env["S3_BUCKET_NAME"]

    final_output_path = path.join(output_path, folder_name)

    if not path.exists(final_output_path):
        logger.info(f"Creating directory {final_output_path}")
        makedirs(final_output_path)

    files = s3_client.list_objects(
        Bucket=bucket_name, Prefix=folder_name)["Contents"]

    for obj in files:
        if obj["Key"].endswith("/"):
            continue

        logger.debug(f"Downloading {obj}")
        file_name = obj["Key"]

        s3_client.download_file(
            bucket_name,
            file_name,
            path.join(output_path, file_name)
        )

        logger.info(
            f"Downloaded {file_name} from S3 bucket {bucket_name} to {output_path}")
