from datetime import datetime
import os
from network_security.constants import training_pipeline
print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m-%d-%Y_%H-%M-%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.pipeline_name,self.artifact_name,timestamp)
        self.timestamp : str= timestamp


class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_dir = os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR)
        self.feature_store_file_path = os.path.join(self.feature_store_dir,training_pipeline.FILE_NAME)
        self.ingested_dir = os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR)
        self.train_file_name = training_pipeline.TRAIN_FILE_NAME
        self.test_file_name  = training_pipeline.TEST_FILE_NAME
        self.training_file_path = os.path.join(self.ingested_dir,self.train_file_name)
        self.testing_file_path = os.path.join(self.ingested_dir,self.test_file_name)  
        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name : str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name : str = training_pipeline.DATA_INGESTION_DATABASE_NAME


class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir:str = os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME
        )
        self.valid_dir:str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_dir:str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path:str = os.path.join(self.valid_dir,training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path:str = os.path.join(self.valid_dir,training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path:str = os.path.join(self.invalid_dir,training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path:str= os.path.join(self.invalid_dir,training_pipeline.TEST_FILE_NAME)
        # self.drift_report_dir :str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR)
        self.drift_report_file_path :str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME
        )

        # Paths for transformed train and test files
        self.transformed_train_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv","npy")
        )
        self.transformed_test_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv","npy")
        )

        # Path for storing transformation objects (like encoders, scalers, etc.)
        self.transformation_object_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.DATA_TRANSFORMATION_PREPROCESSING_OBJECT_FILE_NAME
        )
