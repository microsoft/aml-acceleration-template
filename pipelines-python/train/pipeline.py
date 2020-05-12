import os
import azureml.core
from azureml.core import Workspace, Experiment, Datastore, Dataset, RunConfiguration

from azureml.pipeline.core import Pipeline
from azureml.pipeline.steps import PythonScriptStep

dataset_name =  os.getenv('DATASET', 'german-credit-filedataset')
dataset_mountpath = os.getenv('DATASET_MOUNTPATH', '/data')
source_directory = os.getenv('SOURCE_DIRECTORY', '../../src/model1/')
runconfig = os.getenv('RUNCONFIG', 'pipeline.runconfig')

print("SDK version:", azureml.core.VERSION)

ws = Workspace.from_config()
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep = '\n')

input_ds = Dataset.get_by_name(ws, dataset_name)
training_data = input_ds.as_named_input('training_dataset').as_mount(path_on_compute=dataset_mountpath)

runconfig = RunConfiguration.load(runconfig)

train_step = PythonScriptStep(name="train-step",
                        source_directory=source_directory,
                        runconfig=runconfig,
                        inputs=[training_data],
                        script_name=runconfig.script,
                        arguments=runconfig.arguments,
                        allow_reuse=False)

steps = [train_step]

pipeline = Pipeline(workspace=ws, steps=steps)
pipeline.validate()

pipeline_run = Experiment(ws, 'train-pipe').submit(pipeline)
pipeline_run.wait_for_completion()

#published_pipeline = pipeline.publish(pipeline_name)
#print("Published pipeline id: ", published_pipeline.id)
