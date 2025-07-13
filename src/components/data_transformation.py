from src.exception.exception import CustomException
from src.logging.logger import logging
from src.constent import training_pipeline
from dataclasses import dataclass
from src.components.data_ingestion import DataIngestionArtifact
from src.utils.data_cleaner import DataCleaner
from src.utils.fiel_handler import save_object,save_csv_files

import numpy as np
import pandas as pd
import os,sys


class DataTransformationConfig:
    def __init__(self):
        try:
            transform_dir_path:str=os.path.join(training_pipeline.ARTIFACT_DIR_NAME,training_pipeline.TRANSFORMED_DATASET_DIR_NAME)
            train_transformed_file_path:str=os.path.join(transform_dir_path,training_pipeline.TRAIN_FILE_NAME)
            test_transformed_file_path:str=os.path.join(transform_dir_path,training_pipeline.TEST_FILE_NAME)
            preprocessor_file_path:str=os.path.join(
                training_pipeline.ARTIFACT_DIR_NAME,
                training_pipeline.PICKLE_DIR_NAME,
                training_pipeline.PREPROCESSOR_FILE_NAME
            )
        except Exception as e:
            raise CustomException(e,sys)

@dataclass
class DataTransformationArtifact:
    train_transformed_file_path:str
    test_transformed_file_path:str 
    preprocessor_file_path:str   


class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_cleaner=DataCleaner()
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Reading train_df and test_df in Data Transformation")
            train_df=pd.read_csv(self.data_ingestion_artifact.train_set_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_set_file_path)

            logging.info("Data cleaning process initiated")
            train_df=self.data_cleaner.initiate_data_cleaning(train_df)
            test_df=self.data_cleaner.initiate_data_cleaning(test_df)

            logging.info("Data cleaning object saving...")
            save_object(file_path=self.data_transformation_config.preprocessor_file_path,obj=self.data_cleaner)

            logging.info("Saving transformed datas")
            save_csv_files(self.data_transformation_config.train_transformed_file_path,dataFrame=train_df)
            save_csv_files(self.data_transformation_config.test_transformed_file_path,dataFrame=test_df)


            return DataTransformationArtifact(
                train_transformed_file_path=self.data_transformation_config.train_transformed_file_path,
                test_transformed_file_path=self.data_transformation_config.test_transformed_file_path,
                preprocessor_file_path=self.data_transformation_config.preprocessor_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)