import json
import os
import numpy as np
import pandas as pd
import joblib

def init():
    global model
    
    # Update to your model's filename
    model_filename = "model.pkl"

    # AZUREML_MODEL_DIR is injected by AML
    model_dir = os.getenv('AZUREML_MODEL_DIR')

    print("Model dir:", model_dir)
    print("Model filename:", model_filename)
    
    model_path = os.path.join(model_dir, model_filename)

    # Replace this line with your model loading code
    model = joblib.load(model_path)

def run(raw_data):
    try:
        # Replace this code with your inferencing code
        data = json.loads(raw_data)['data']
        input_df = pd.DataFrame.from_dict(data)
        proba = model.predict_proba(input_df)
        
        result = {"predict_proba": proba.tolist()}
        return result
    except Exception as e:
        error = str(e)
        return error
