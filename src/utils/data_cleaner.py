from src.logging.logger import logging
from src.exception.exception import CustomException
from typing import List

import pandas as pd
import numpy as np
import os,sys

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


class DataCleaner:
    def __init__(self):
        try:
            self.stopwords=stopwords.words('english')
            self.stopwords.remove('not')
            logging.info("Stopwords loaded")
        except Exception as e:
            logging.info("Failed to load stopwords")
    def concat_text_title_in_dataframes(self,dataframe:pd.DataFrame)->pd.DataFrame:
        try:
            logging.info("Title-Text concatination")
            dataframe["title_text"]=dataframe.title+' '+dataframe.text
            dataframe.drop("title",axis=1,inplace=True)
            dataframe.drop("text",axis=1,inplace=True)
            return dataframe
        except Exception as e:
            raise CustomException(e,sys)

    def date_extraction(self,dataframe:pd.DataFrame)->pd.DataFrame:
        try:
            logging.info("Date extraction")
            dataframe["year"]=dataframe.date.str.split(',').str[1]
            dataframe.year.fillna('2018',inplace=True)
            dataframe.year=dataframe.year.str.strip()
            dataframe.year=dataframe.year.astype(np.int64)
            dataframe.drop('date',inplace=True,axis=1)
            return dataframe
        except Exception as e:
            raise CustomException(e,sys)
    def text_cleaner(self,text)->List:
        try:
            corpus=[]
            for t in text:
                t=re.sub('[^a-zA-Z]',' ',t)
                t=t.lower()
                t=t.split()
                ps=PorterStemmer()
                t=[ps.stem(word) for word in t if word not in set(self.stopwords)]
                t=' '.join(t)
                corpus.append(t)
            return corpus
        except Exception as e:
            raise CustomException(e,sys)
    def vectorizer(self,corpus:List):
        try:
            vecto=TfidfVectorizer(max_features=25000,min_df=5,max_df=0.7)
            vect_arr=vecto.fit_transform(corpus).toarray()
            return vect_arr
        except Exception as e:
            raise CustomException(e,sys)
    
    def feature_reduction(self,vectorizerd_array,n_components:int=300):
        try:
            feature_reducer=TruncatedSVD(n_components=n_components)
            vectorizerd_array=feature_reducer.fit_transform(vectorizerd_array)
            return vectorizerd_array
        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_data_cleaning(self,dataset:pd.DataFrame)->pd.DataFrame:
        try:
            dataset=self.concat_text_title_in_dataframes(dataframe=dataset)
            dataset=self.date_extraction(dataframe=dataset)

            logging.info("Text cleaning initiated")
            corpus=self.text_cleaner(text=dataset['title_text'])

            vect_arr=self.vectorizer(corpus=corpus)
            vect_arr=self.feature_reduction(vectorizerd_array=vect_arr)

            return_df=pd.DataFrame(vect_arr)
            return_df["year"]=dataset.year
            return_df["IsFake"]=dataset.IsFake

            return return_df
        except Exception as e:
            raise CustomException(e,sys)