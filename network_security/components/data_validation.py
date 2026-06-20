from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.artifiact_entity import DataIngestionArtifact,DataValidationArtifact
from network_security.entity.config_entity import DataValidationConfig,TrainingPipelineConfig
from scipy.stats import ks_2samp
from network_security.constants import SCHEMA_FILE_NAME
from network_security.utils.main_utils.utils import read_yaml_file,write_yaml_file
import os,sys
import pandas as pd

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_NAME)
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
        
    def detect_data_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1  = base_df[column]
                d2 = current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                }})
            drift_report_dir = os.path.dirname(self.data_validation_config.drift_report_file_path)
            os.makedirs(drift_report_dir,exist_ok=True)
            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path,content=report)
            return status
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
        
    def initialize_data_validation(self)-> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.testing_file_path

            #read the data
            train_dataFrame = DataValidation.read_data(train_file_path)
            test_dataFrame = DataValidation.read_data(test_file_path)
            status = self.validate_number_of_columns(train_dataFrame)
            if not status:
                raise Exception("Train data does not have all the required columns")
            status = self.validate_number_of_columns(test_dataFrame)
            if not status:
                raise Exception("Test data does not have all the required columns")
            
            #lets check datasrift
            status = self.detect_data_drift(base_df=train_dataFrame,current_df=test_dataFrame)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataFrame.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_dataFrame.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)
            data_validation_artifact = DataValidationArtifact(
                validation_status = status,
                valid_train_file_path = self.data_validation_config.valid_train_file_path,
                valid_test_file_path = self.data_validation_config.valid_test_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e