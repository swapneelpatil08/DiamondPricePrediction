"""Module providing a function to log all activities."""
import os
import sys
from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import CustomException

# Initialize the Data ingestion configuration.

@dataclass
class DataIngestionConfig:
    """Class representing Data Ingestion Config"""
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'raw.csv')

class DataIngestion:
    """Class representing Data Ingestion"""
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        """initiate data ingestion"""
        logging.info("Data ingestion method initiated")
        try:
            df = pd.read_csv(os.path.join("notebooks/data", "diamonds.csv"))
            logging.info("Dataset read from using pandas Dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path)

            logging.info("Raw data is created")

            train_set, test_set = train_test_split(df, test_size=0.30, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Ingestion of data is completed.")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            logging.info("Exception occured at Data Ingestion Stage")
            raise CustomException(e, sys) from e

    def do_not(self):
        """TP"""
        return True
