import os
import argparse
import azureml.core
from azureml.core import Workspace
from azureml.pipeline.core import Pipeline, PublishedPipeline, PipelineEndpoint

print("Azure ML SDK version:", azureml.core.VERSION)

parser = argparse.ArgumentParser("publish_to_pipeline_endpoint")
parser.add_argument("--pipeline_id", type=str, help="Id of the published pipeline that should get added to the Pipeline Endpoint", required=True)
parser.add_argument("--pipeline_endpoint_name", type=str, help="Name of the Pipeline Endpoint that the the pipeline should be added to", required=True)
args = parser.parse_args()
print(f'Arguments: {args}')

print('Connecting to workspace')
ws = Workspace.from_config()
print(f'WS name: {ws.name}\nRegion: {ws.location}\nSubscription id: {ws.subscription_id}\nResource group: {ws.resource_group}')

# Connect to the workspace
ws = Workspace.from_config()
print(f'WS name: {ws.name}')
print(f'Region: {ws.location}')
print(f'Subscription id: {ws.subscription_id}')
print(f'Resource group: {ws.resource_group}')

endpoint_name = args.pipeline_endpoint_name
pipeline_id = args.pipeline_id
published_pipeline = PublishedPipeline.get(workspace=ws, id=pipeline_id)

# Add tested published pipeline to pipeline endpoint
try:
    pl_endpoint = PipelineEndpoint.get(workspace=ws, name=endpoint_name)
    pl_endpoint.add_default(published_pipeline)
    print(f'Added pipeline {pipeline_id} to Pipeline Endpoint with name {endpoint_name}')
except Exception:
    print(f'Will create new Pipeline Endpoint with name {endpoint_name} with pipeline {pipeline_id}')
    pl_endpoint = PipelineEndpoint.publish(workspace=ws,
                                           name=endpoint_name,
                                           pipeline=published_pipeline,
                                           description="New Training Pipeline Endpoint")
