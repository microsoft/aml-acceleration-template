import os
import argparse
import azureml.core
from azureml.core import Workspace, Experiment, Datastore, Dataset, RunConfiguration
from azureml.core.compute import AmlCompute
from azureml.core.compute import ComputeTarget
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.authentication import AzureCliAuthentication
print("Pipeline SDK-specific imports completed")
# Check core SDK version number
print("Azure ML SDK version:", azureml.core.VERSION)

parser = argparse.ArgumentParser("pipelines_master")
parser.add_argument("--model_name", type=str, help="model name", dest="model_name", required=True)
parser.add_argument("--build_number", type=str, help="build number", dest="build_number", required=False)
parser.add_argument("--image_name", type=str, help="image name", dest="image_name", required=True)
parser.add_argument("--path", type=str, help="path", dest="path", required=True)
parser.add_argument("--dataset", type=str, help="dataset", dest="dataset", required=True)
parser.add_argument("--dataset_mountpath", type=str, help="dataset_mountpath", dest="dataset_mountpath", required=True)
parser.add_argument("--runconfig", type=str, help="runconfig", dest="runconfig", required=True)
parser.add_argument("--source_directory", type=str, help="source_directory", dest="source_directory", required=True)
args = parser.parse_args()

#dataset_name =  os.getenv('DATASET', 'german-credit-filedataset')
#dataset_mountpath = os.getenv('DATASET_MOUNTPATH', '/data')
#source_directory = os.getenv('SOURCE_DIRECTORY', '../../src/model1/')
#runconfig = os.getenv('RUNCONFIG', 'pipeline.runconfig')


print("Argument source_directory %s" % args.source_directory)
print("Argument model_name: %s" % args.model_name)
print("Argument build_number: %s" % args.build_number)
print("Argument image_name: %s" % args.image_name)
print("Argument path: %s" % args.path)
print("Argument dataset: %s" % args.dataset)
print("Argument dataset_mountpath: %s" % args.dataset_mountpath)
print("Argument runconfig: %s" % args.runconfig)

print('creating AzureCliAuthentication...')
cli_auth = AzureCliAuthentication()
print('done creating AzureCliAuthentication!')

print('get workspace...')
ws = Workspace.from_config(path=args.path, auth=cli_auth)
print('Workspace name: ' + ws.name, 
      'Azure region: ' + ws.location, 
      'Subscription id: ' + ws.subscription_id, 
      'Resource group: ' + ws.resource_group, sep = '\n')
      
print('done getting workspace!')



scripts_folder = 'scripts'
def_blob_store = ws.get_default_datastore()

train_output = PipelineData('train_output', datastore=def_blob_store)
print("train_output PipelineData object created")

print('--------------------------')
print(args.runconfig)
runconfig = RunConfiguration.load(args.runconfig)
print('--------------------------')

print("setup dataset")    
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

pipeline = Pipeline(workspace=ws, steps=steps)
pipeline.validate()
print("pipeline validation complete")
#pipeline_run = Experiment(ws, 'train-pipe').submit(pipeline)
#pipeline_run.wait_for_completion()

published_pipeline = pipeline.publish(args.model_name)
print("Published pipeline id: ", published_pipeline.id)
