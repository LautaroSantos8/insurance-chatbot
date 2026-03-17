import boto3
from common.logger import logger
from dotenv import dotenv_values


class AWSClients:
    """
    A singleton class for creating and accessing different AWS clients.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.s3_client = cls._instance.__init__()
        return cls._instance

    def __init__(self):
        """
        Initializes the AWS S3 client using the AWS credentials from the .env file.

        Raises:
            Exception: If the S3 client initialization fails.
        """
        try:
            env = dotenv_values()
            s3_client: boto3.session.Session.client = boto3.client(
                service_name='s3',
                aws_secret_access_key=env["S3_SECRET_ACCESS_KEY"],
                aws_access_key_id=env["S3_ACCESS_KEY_ID"],
            )

            self.s3_client = s3_client
            logger.debug("S3 client initialized successfully.")

        except Exception as e:
            logger.error(f"Error: {e}")
            raise ("Error: S3 client initialization failed.")

    def get_s3_client(self):
        """
        Returns the AWS S3 client.

        Returns:
            boto3.session.Session.client: The AWS S3 client.
        """
        return self.s3_client
