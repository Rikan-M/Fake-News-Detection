import os

TARGET_COLUMN:str="isFake"

FAKE_DATASET_PATH:str='notebook\Fake.csv'
TRUE_DATASET_PATH:str='notebook\True.csv'

TRAIN_TEST_SPLIT_RATIO:float=0.2


TRAIN_FILE_NAME='train.csv'
TEST_FILE_NAME='test.csv'
TOTAL_DATASET_FILE_NAME='total.csv'



ARTIFACT_DIR_NAME='artifacts'

DATASET_DIR_NAME='dataset'
FULL_DATASET_DIR_NAME='total_dataset'
TRAIN_TEST_DATASET_DIR_NAME='train_test_dataset'

PICKLE_DIR_NAME='pickle_data'
PREDICTION_PIPELINE_DIR='prediction_pipeline'
PREDICTION_MODEL_FILE_NAME='predict.pkl'
PREPROCESSOR_FILE_NAME='preprocessor.pkl'

TRANSFORMED_DATASET_DIR_NAME='transformed'


PREDICTION_MODEL_PATH:str=os.path.join(
    ARTIFACT_DIR_NAME,PICKLE_DIR_NAME,PREDICTION_MODEL_FILE_NAME
)


