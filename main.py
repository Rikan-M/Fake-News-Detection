from src.components.data_ingestion import DataIngestion,DataIngestionConfig
from src.exception.exception import CustomException
from src.constent import training_pipeline


import sys



if __name__=='__main__':
    try:
        dataingestion_config=DataIngestionConfig()
        dataingestion_obj=DataIngestion(dataingestion_config)
        dataingestion_artifact=dataingestion_obj.initiate_data_ingestion()
    except Exception as e:
        raise CustomException(e,sys)
