# Commands to run this repo

This document shares the commands on how to run training and real-time inferencing locally and on Azure Machine Learning (AML).

## Attaching to workspace

Attach the folder with the model code to the AML workspace (run this command from `src/model1/`):
```
az ml folder attach -g aml-demo-we -w aml-demo-we
```

This connects the model folder to the workspace in AML.

## Training

Train locally with Python (without AML):
```
python train.py --data-path ../../sample-data/
```

Train on local Docker container, but log metrics to AML:
```
az ml run submit-script -c train-local -e aml-poc-local
```

Train using AML on AML Compute Cluster:
```
az ml run submit-script -c train-amlcompute -e aml-poc-amlcompute
```

## Model management

Register model to model registry in AML (from local path):
```
az ml model register -n demo-model --asset-path outputs/model.pkl
```

Get latest model version:
```
az ml model list -n demo-model --query '[0].version'
```

## Model deployment

### Deploy model to local Docker container

Deploy model to local Docker container:
```
az ml model deploy -n test-deploy -m demo-model:1 --ic aml_config/inference-config.yml --dc aml_config/deployment-config-aci.yml --runtime python --compute-type local --port 32000 --overwrite
```

Delete locally deployed model:
```
az ml service delete --name test-deploy
```

### Deploy model to Azure Container Instances in Azure

Deploy model to Azure Container Instances (ACI):
```
az ml model deploy -n test-deploy-aci -m demo-model:1 --ic amlconfig/inference-config.yml --dc amlconfig/deployment-config-aci.yml --overwrite
```

Delete ACI deployed model:
```
az ml service delete --name test-deploy-aci
```

### Deploy model to Azure Kubernetes Service in Azure

Deploy model to Azure Kubernetes Service (AKS):
```
az ml model deploy -n test-deploy-aks --ct aks-cluster -m demo-model:1 --ic amlconfig/inference-config.yml --dc amlconfig/deployment-config-aks.yml --overwrite
```

Delete AKS deployed model:
```
az ml service delete --name test-deploy-aks
```

## Pipeline execution

Execute pipeline (need to be ran from inside the pipeline folders):

```
az ml run submit-pipeline -n pipeline-test-exp -y pipeline.yml
```

