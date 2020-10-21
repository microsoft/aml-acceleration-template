import os
import argparse
import azureml.core
from azureml.core import Workspace
from azureml.pipeline.core import Pipeline, PublishedPipeline, PipelineEndpoint

print("Azure ML SDK version:", azureml.core.VERSION)

parser = argparse.ArgumentParser("publish_to_pipeline_endpoint")
parser.add_argument("--pipeline_id", type=str, help="Id of the published pipeline that should get added to the Pipeline Endpoint", required=True)
parser.add_argument("--pipeline_endpoint", type=str, help="Name of the Pipeline Endpoint that the the pipeline should be added to", required=True)
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

endpoint_name = args.pipeline_endpoint
pipeline_id = args.pipeline_id
published_pipeline = PublishedPipeline.get(workspace=ws, id=pipeline_id)

# Check if PipelineEndpoint already exists
if any(pe.name == endpoint_name for pe in PipelineEndpoint.list(ws)):
    print(f'Pipeline Endpoint with name {endpoint_name} already exists, will add pipeline {pipeline_id} to it')
    pipeline_endpoint = PipelineEndpoint.get(workspace=ws, name=endpoint_name)
    pipeline_endpoint.add(published_pipeline)
    # Set it to default, as we already tested it beforehand
    pipeline_endpoint.set_default(published_pipeline)
else:
    print(f'Will create new Pipeline Endpoint with name {endpoint_name} and add pipeline {pipeline_id} to it')
    pipeline_endpoint = PipelineEndpoint.publish(workspace=ws,
                                                name=endpoint_name,
                                                pipeline=published_pipeline,
                                                description="New Training Pipeline Endpoint")