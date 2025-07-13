import dill
import sys,os
from src.exception.exception import CustomException
import pandas as pd

def save_csv_files(file_path:str,dataFrame:pd.DataFrame)->None:
    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        dataFrame.to_csv(file_path,index=False,header=True)
    except Exception as e:
        raise CustomException(e,sys)



def save_object(file_path:str,obj)->None:
    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,'wb') as f:
            dill.dump(obj=obj,file=f)
    except Exception as e:
        raise CustomException(e,sys)

def load_object(file_path:str):
    try:
        with open(file_path,'rb') as f:
            return dill.load(file=f)

    except Exception as e:
        raise CustomException(e,sys)
    