from src.exception.exception import CustomException
from src.logging.logger import logging
import pandas as pd
import os,sys




class PredictPipeline:
    def __init__(self,preprocessor,model):
        self.preprocessor=preprocessor
        self.model=model
    def make_dataframe(self,title,text,date)->pd.DataFrame:
        try:
            data={
                "title":[title],
                "text":[text],
                "date":[date]
            }
            return pd.DataFrame(data)
        except Exception as e:
            raise CustomException(e,sys)
    def predict(self,title,text,date):
        try:
            dataframe=self.make_dataframe(title=title,text=text,date=date)
            preprocessed:pd.DataFrame=self.preprocessor.initiate_data_cleaning(dataset=dataframe,is_train_data=False)
            x_pred=preprocessed.values
            y_pred=self.model.predict(x_pred)
            return y_pred
        except Exception as e:
            raise CustomException(e,sys)
