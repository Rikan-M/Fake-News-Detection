from dataclasses import dataclass
from src.exception.exception import CustomException
from src.logging.logger import logging
from src.constent import training_pipeline
from src.utils.fiel_handler import save_csv_files
from sklearn.model_selection import train_test_split
import pandas as pd
import os,sys



class DataIngestionConfig:
    def __init__(self):
        try:
            train_test_split_ratio:float=training_pipeline.TRAIN_TEST_SPLIT_RATIO
            fake_dataset_file_path:str=training_pipeline.FAKE_DATASET_PATH
            true_dataset_file_path:str=training_pipeline.TRUE_DATASET_PATH
            dataset_dir_path:str=os.path.join(
                training_pipeline.ARTIFACT_DIR_NAME,
                training_pipeline.DATASET_DIR_NAME
            )
            total_set_file_path:str=os.path.join(
                dataset_dir_path,
                training_pipeline.FULL_DATASET_DIR_NAME,
                training_pipeline.TOTAL_DATASET_FILE_NAME
            )
            train_set_file_path:str=os.path.join(
                dataset_dir_path,
                training_pipeline.TRAIN_TEST_DATASET_DIR_NAME,
                training_pipeline.TRAIN_FILE_NAME
            )
            test_set_file_path:str=os.path.join(
                dataset_dir_path,
                training_pipeline.TRAIN_TEST_DATASET_DIR_NAME,
                training_pipeline.TEST_FILE_NAME
            )
        except Exception as e:
            raise CustomException(e,sys)


@dataclass
class DataIngestionArtifact:
    train_set_file_path:str
    test_set_file_path:str


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)
    def combine_csv_files(self,fake_file_path,true_file_path):
        try:
            logging.info("Importing true and fake df")
            fake_df=pd.read_csv(fake_file_path)
            true_df=pd.read_csv(true_file_path)
            fake_df['isFake']=1
            true_df['isFake']=0
            logging.info("Combining true and fake df into one single df")
            df=pd.concat((fake_df,true_df),axis=0)
            df.drop("subject",axis=1,inplace=True)
            return df
        except Exception as e:
            raise CustomException(e,sys)
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            df=self.combine_csv_files(
                fake_file_path=self.data_ingestion_config.fake_dataset_file_path,
                true_file_path=self.data_ingestion_config.true_dataset_file_path
            )

            logging.info("Checking and creating Directories")

            os.makedirs(os.path.dirname(self.data_ingestion_config.train_set_file_path),exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.total_set_file_path),exist_ok=True)

            save_csv_files(file_path=self.data_ingestion_config.total_set_file_path,dataFrame=df)

            logging.info("Total dataset saved")

            train_set,test_set=train_test_split(df,
                                                test_size=self.data_ingestion_config.train_test_split_ratio,
                                                random_state=42
                                                )
            logging.info("Exporting training set & test set")
            save_csv_files(file_path=self.data_ingestion_config.train_set_file_path,dataFrame=train_set)
            save_csv_files(file_path=self.data_ingestion_config.test_set_file_path,dataFrame=test_set)

            return DataIngestionArtifact(train_set_file_path=self.data_ingestion_config.train_set_file_path,
                                         test_set_file_path=self.data_ingestion_config.test_set_file_path)
        except Exception as e:
            raise CustomException(e,sys)
