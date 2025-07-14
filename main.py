from src.components.data_ingestion import (DataIngestion,DataIngestionConfig,DataIngestionArtifact)
from src.exception.exception import CustomException
from src.components.data_transformation import (DataTransformation,DataTransformationConfig,DataTransformationArtifact)
from src.components.model_trainer import (ModelTrainerConfig,ModelTrainer)
from src.constent import training_pipeline

import sys

if __name__=='__main__':
    try:
        dataingestion_config=DataIngestionConfig()
        dataingestion_obj=DataIngestion(dataingestion_config)
        dataingestion_artifact:DataIngestionArtifact=dataingestion_obj.initiate_data_ingestion()

        data_transformation_config=DataTransformationConfig()
        data_transformation_obj=DataTransformation(data_transformation_config=data_transformation_config,
                                                   data_ingestion_artifact=dataingestion_artifact)
        data_transformation_artifact:DataTransformationArtifact=data_transformation_obj.initiate_data_transformation()

        model_trainer_config=ModelTrainerConfig()
        model_trainer_obj=ModelTrainer(model_trainer_config=model_trainer_config,
                                       data_transformation_artifact=data_transformation_artifact)
        name,score=model_trainer_obj.initiate_model_trainer()
        print(f"{name} : {score}")
    except Exception as e:
        raise CustomException(e,sys)
