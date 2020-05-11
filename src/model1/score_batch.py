import os
import glob
import json
import argparse
import numpy as np
import pandas as pd
import joblib
from azureml.core.model import Model

model_name = "demo-model"

def init():
    global model
    
    model_path = Model.get_model_path(model_name)
    model = joblib.load(model_path)

def run(file_list):
    try:
        output_df = pd.DataFrame(columns=["Sno", "ProbaGoodCredit", "ProbaBadCredit"])
        for filename in file_list:
            df = pd.read_csv(filename)

            sno = df["Sno"]
            df = df.drop("Sno", axis=1)

            proba = model.predict_proba(df)
            proba = pd.DataFrame(data=proba, columns=["ProbaGoodCredit", "ProbaBadCredit"])
            result = pd.concat([sno, proba], axis=1)
            output_df = output_df.append(result)

            print("Batch scored: ", filename)

        return output_df
    except Exception as e:
        error = str(e)
        return error

def test():
    global model
    model = joblib.load("./outputs/model.pkl")

    # Simulate AML ingesting paths to the data files
    files = ['../../sample-data/german_credit_data_batch_test.csv']
    result = run(files)
    print(result)

if __name__ == "__main__":
    test()
