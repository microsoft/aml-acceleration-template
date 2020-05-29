import os
import argparse
import azureml.core
from azureml.core import Workspace, Experiment, Datastore, Dataset, RunConfiguration
from azureml.core.compute import AmlCompute
from azureml.core.compute import ComputeTarget
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.authentication import AzureCliAuthentication

print("Azure ML SDK version:", azureml.core.VERSION)

parser = argparse.ArgumentParser("deploy_training_pipeline")
parser.add_argument("--pipeline_name", type=str, help="Name of the pipeline that will be deployed", dest="pipeline_name", required=True)
parser.add_argument("--build_number", type=str, help="Build number", dest="build_number", required=False)
parser.add_argument("--dataset", type=str, help="Dataset name", dest="dataset", required=True)
parser.add_argument("--dataset_mountpath", type=str, help="Dataset mount path on AML Compute Cluster", dest="dataset_mountpath", required=True)
parser.add_argument("--runconfig", type=str, help="Path to runconfig for pipeline", dest="runconfig", required=True)
parser.add_argument("--source_directory", type=str, help="Path to model training code", dest="source_directory", required=True)
args = parser.parse_args()
print(f'Arguments: {args}')

print('Connecting to workspace')
cli_auth = AzureCliAuthentication()
ws = Workspace.from_config(auth=cli_auth)
print(f'WS name: {ws.name}\nRegion: {ws.location}\nSubscription id: {ws.subscription_id}\nResource group: {ws.resource_group}')

print('Loading runconfig for pipeline')
runconfig = RunConfiguration.load(args.runconfig)

print('Loading dataset')    
input_ds = Dataset.get_by_name(ws, args.dataset)
training_data = input_ds.as_named_input('training_dataset').as_mount(path_on_compute=args.dataset_mountpath)

train_step = PythonScriptStep(name="train-step",
                        source_directory=args.source_directory,
                        runconfig=runconfig,
                        inputs=[training_data],
                        script_name=runconfig.script,
                        arguments=runconfig.arguments,
                        allow_reuse=False)

steps = [train_step]

print('Creating and validating pipeline')
pipeline = Pipeline(workspace=ws, steps=steps)
pipeline.validate()

print('Publishing pipeline')
published_pipeline = pipeline.publish(args.pipeline_name)
print(f'Published pipeline id: {published_pipeline.id}')

#pipeline_run = Experiment(ws, 'training-pipe').submit(pipeline)
#pipeline_run.wait_for_completion()