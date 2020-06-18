# Automation

This folder features multiple CI/CD pipelines for automating various tasks in the MLOps process. However, these pipelines are often very use case specific, hence often need to be adapted to your needs.

## `Training, Deploy, Test` pipeline

Filename: [deploy-ml-train-pipeline.yml](deploy-ml-train-pipeline.yml)

This Azure DevOps pipeline shows an example for the current flow:

1. Train model
1. Register model
1. Deploy model
1. Run automated tests against the deployed model

As an outcome, this pipeline creates a deployed model that has been tested and can be consumed by an application or user.

## `Deploy ML pipeline` pipeline

Filename: [deploy-ml-train-pipeline.yml](deploy-ml-train-pipeline.yml)

This Azure DevOps pipeline shows an example for the current flow:

1. Deploy ML training pipeline
1. Tested deployed ML pipeline with a small training set

As an outcome, this pipeline deploys a ML training pipeline that can be triggered by another application or user to (re)train a model.