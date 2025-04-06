import os
import pandas as pd
import boto3
from src.logger import get_logger 
from src.custom_exception import CustomException 
from config.paths_config import * 
from utils.common_functions import read_yaml 

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config['data_ingestion']
        self.bucket_name = self.config['bucket_name']
        self.file_names = self.config['bucket_file_names']
        
        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f"Data Ingestion started with {self.bucket_name}")
    
    def download_csv_from_gcp(self):
        try:
            s3_client = boto3.client("s3",
                                     endpoint_url="http://localhost:9000",
                                     aws_access_key_id="minioadmin",
                                     aws_secret_access_key="minioadmin"
                                     )
            for file_name in self.file_names:
                file_path = os.path.join(RAW_DIR, file_name)
                
                if file_name=="animelist.csv":
                    s3_client.download_file(self.bucket_name,file_name,file_path)
                    
                    data =pd.read_csv(file_path, nrows=5000000)
                    data.to_csv(file_path, index=False)
                    logger.info("Large file detected only downloading 5M rows")
                else:
                    s3_client.download_file(self.bucket_name,file_name,file_path)
                    
                    logger.info("Downloading small files")
        except Exception as e:
            logger.error("Error while downloading data from storage")
            raise CustomException("Failed to download data", e)
    
    def run(self):
        try:
            logger.info("Starting data ingestion process")
            self.download_csv_from_gcp()
            logger.info("Data ingestion completed successfully")
        except CustomException as ce:
            logger.error(f"CustomException: {str(ce)}")
        finally:
            logger.info("Data ingestion completed")

if __name__=="__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()
    