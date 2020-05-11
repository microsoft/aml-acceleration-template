# Inferencing

1. Adapt conda enviroment for inferencing
    * Copy your dependencies from [`aml_config/train-conda.yml`](../src/model1/aml_config/train-conda.yml) to [`aml_config/inference-conda.yml`](../src/model1/aml_config/inference-conda.yml)
    * If you have different dependencies for inferencing, you can adapt them in [`aml_config/inference-conda.yml`](../src/model1/aml_config/train-conda.yml)

1. Adapt existing `score.py`
    * TODO: More details?
    * Open `score.py` and start updating the `init()` and `run()` methods with the instructions given in the file

1. Deploy model as a RESTful service to local host 
    * Deploy locally to Docker:
    ```
    az ml model deploy -n test-deploy -m demo-model:1 --ic aml_config/inference-config.yml --dc aml_config/deployment-config-aci.yml --runtime python --compute-type local --port 32000 --overwrite
    ```

1. Test if the model works
    * `POST` a sample request to your local endpoint using Postman, curl, etc.
    * TODO: More guidance needed?
    * The model used in the template can be accessed using the following syntax:
    ```
    POST http://localhost:32000/score HTTP/1.1
    Content-Type: application/json

    { 
        "data": [
            {
            "Age": 20,
            "Sex": "male",
            "Job": 0,
            "Housing": "own",
            "Saving accounts": "little",
            "Checking account": "little",
            "Credit amount": 100,
            "Duration": 48,
            "Purpose": "radio/TV"
            }
        ]
    }
    ```
    * Once it is working, you can delete the locally deployed service
    ```
    az ml service delete --name test-deploy
    ```

1. Deploy model to ACI for testing the model in Azure
    * Finally, you can test deploying the model to ACI
    ```
    az ml model deploy -n test-deploy-aci -m demo-model:1 --ic amlconfig/inference-config.yml --dc amlconfig/deployment-config-aci.yml --overwrite
    ```
    * TODO: Add example how to test it

1. Deploy model to AKS
    * TODO write up fully


Great, the model is running a service, let's move on the [next section](03-pipelines.md) and look how we can run ML Pipelines for automation on Azure.