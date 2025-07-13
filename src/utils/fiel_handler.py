import dill
import sys,os
from src.exception.exception import CustomException

def save_object(file_path:str,obj):
    try:
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
    