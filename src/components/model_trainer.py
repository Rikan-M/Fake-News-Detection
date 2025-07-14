from src.exception.exception import CustomException
from src.logging.logger import logging
from src.components.data_transformation import DataTransformationArtifact
from src.utils.fiel_handler import save_object,load_object
from src.constent import training_pipeline
from src.constent.training_pipeline import TARGET_COLUMN

from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from catboost import CatBoostClassifier

from sklearn.model_selection import GridSearchCV

from sklearn.metrics import accuracy_score

import pandas as pd
from dataclasses import dataclass


import os,sys

@dataclass
class ModelTrainerConfig:
    pickle_dir_path:str=os.path.join(
        training_pipeline.ARTIFACT_DIR_NAME,
        training_pipeline.PICKLE_DIR_NAME
                                 )
    model_file_path:str=os.path.join(
        pickle_dir_path,
        training_pipeline.MODEL_FILE_NAME
    )


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
    def data_devider(self,file_path:str):
        try:
            dataframe=pd.read_csv(file_path)
            input_feature_df=dataframe.drop(TARGET_COLUMN,axis=1)
            target_feature_df=dataframe[TARGET_COLUMN]
            return (
                input_feature_df.values,
                target_feature_df.values
            )
        except Exception as e:
            raise CustomException(e,sys)
    
    def model_evaluator(self,model,x_train,y_train,x_test,y_test)->dict:
        try:
            model.fit(x_train,y_train)
            y_pred=model.predict(x_test)
            accuracy=accuracy_score(y_test,y_pred)
            return accuracy
        except Exception as e:
            raise CustomException(e,sys)
        
    
    def model_selector(self,x_train,y_train,x_test,y_test):
        models = {
                "Random Forest": RandomForestClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "Logistic Regression": LogisticRegression(),
                "XGBClassifier": XGBClassifier(),
                "CatBoosting Classifier": CatBoostClassifier(verbose=False),
                "AdaBoost Classifier": AdaBoostClassifier(),
            }
        model_report={}
        for name,model in models.items():
            model_acc=self.model_evaluator(model=model,x_train=x_train,x_test=x_test,y_test=y_test,y_train=y_train)
            model_report[name]=model_acc
        best_model_score=max(sorted(model_report.values()))

        best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        best_model=models[best_model_name]
        return (best_model,best_model_name,best_model_score)
    def initiate_model_trainer(self):
        try:
            logging.info("Read transformed csv files")
            train_input_features,train_target_feature=self.data_devider(self.data_transformation_artifact.train_transformed_file_path)
            test_input_features,test_target_feature=self.data_devider(self.data_transformation_artifact.test_transformed_file_path)
            logging.info("Running model selector")
            model,name,score=self.model_selector(x_train=train_input_features,
                                      y_train=train_target_feature,
                                      x_test=test_input_features,
                                      y_test=test_target_feature)
            model.fit(train_input_features,train_target_feature)
            save_object(file_path=self.model_trainer_config.model_file_path,obj=model)

            return (name,score)
        
        except Exception as e:
            raise CustomException(e,sys)