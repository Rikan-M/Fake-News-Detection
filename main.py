from src.components.data_ingestion import (DataIngestion,DataIngestionConfig,DataIngestionArtifact)
from src.exception.exception import CustomException
from src.components.data_transformation import (DataTransformation,DataTransformationConfig,DataTransformationArtifact)
from src.components.model_trainer import (ModelTrainerConfig,ModelTrainer,ModelTrainerArtifact)
from src.constent import training_pipeline
from src.logging.logger import logging

import sys

if __name__=='__main__':
    try:
        logging.info("Started data ingestion")
        dataingestion_config=DataIngestionConfig()
        dataingestion_obj=DataIngestion(dataingestion_config)
        dataingestion_artifact:DataIngestionArtifact=dataingestion_obj.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        print("="*100)
        print(dataingestion_artifact)


        logging.info("Started data transformation")
        data_transformation_config=DataTransformationConfig()
        data_transformation_obj=DataTransformation(data_transformation_config=data_transformation_config,
                                                   data_ingestion_artifact=dataingestion_artifact)
        data_transformation_artifact:DataTransformationArtifact=data_transformation_obj.initiate_data_transformation()
        logging.info("Data transformation completed")
        print("="*100)
        print(data_transformation_artifact)


        logging.info("Started model training")
        model_trainer_config=ModelTrainerConfig()
        model_trainer_obj=ModelTrainer(model_trainer_config=model_trainer_config,
                                       data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact:ModelTrainerArtifact=model_trainer_obj.initiate_model_trainer()
        logging.info("Model training completed")
        print("="*100)
        print(model_trainer_artifact)
    except Exception as e:
        raise CustomException(e,sys)
