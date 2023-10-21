from sklearn.impute import SimpleImputer # Handling missing values
from sklearn.preprocessing import StandardScaler # Handling feature scaling
from sklearn.preprocessing import OrdinalEncoder # Ordinal encoding
# Pipelines
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
from dataclasses import dataclass

import sys, os

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
    def get_data_transformation_object(self):
        try:
            logging.info("Data Transform initiated")
            
            # Categorical and numerical columns
            categorical_cols = ['cut', 'color', 'clarity']
            numerical_cols = ['carat', 'depth', 'table', 'x','y','z']
            
            # Define the custom ranking for each ordinal variable
            cut_categories = ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal']
            clarity_categories = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            
            logging.info("Data Transform pipeline initiated")
            
            ## Numerical Pipeline
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )


            # Categorical Pipeline
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('ordinalencoder', OrdinalEncoder(categories=[cut_categories, color_categories, clarity_categories])),
                    ('scaler', StandardScaler())
                ]
            )


            preprocessor = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_cols),
                ('cat_pipelines', cat_pipeline, categorical_cols)
            ])
            
            logging.info("Data Transform completed")

            return preprocessor
        
        except Exception as e:
            logging.info('Exception occured in data transformation')
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_data_path, test_data_path):
        try:
            train_df = pd.read_csv(train_data_path)
            test_df = pd.read_csv(test_data_path)
            
            logging.info("Read train and test data completed")
            logging.info(f"Train dataframe head: \n{train_df.head().to_string()}")
            logging.info(f"Test dataframe head: \n{test_df.head().to_string()}")
            
            logging.info("Create preprocessing object")

            preprocessing_obj = self.get_data_transformation_object()
            
            target_column = 'price'
            drop_cols = [target_column]
            
            # Dividing the dataset into independent and dependent feature
            # Training Data
            input_feature_train_df = train_df.drop(columns=drop_cols, axis=1)
            target_feature_train_df = train_df[target_column]
            
            # Test Data
            input_feature_test_df = test_df.drop(columns=drop_cols, axis=1)
            target_feature_test_df = test_df[target_column]
            
            # Data transformation
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.fit_transform(input_feature_test_df)
            
            logging.info("Applying preprocessing object on training ad testing datasets")
            
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)