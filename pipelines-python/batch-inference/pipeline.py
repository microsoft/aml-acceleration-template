import os
import azureml.core
from azureml.core import Workspace, Experiment, Datastore, Dataset, RunConfiguration, Model
from azureml.core.compute import AmlCompute
from azureml.pipeline.core import Pipeline, PipelineData

from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.contrib.pipeline.steps import ParallelRunConfig 
from azureml.contrib.pipeline.steps import ParallelRunStep 

dataset_name =  os.getenv('DATASET', 'german-credit-filedataset')
source_directory = os.getenv('SOURCE_DIRECTORY', '../../src/model1/')
runconfig = os.getenv('RUNCONFIG', 'pipeline.runconfig')
model_name = os.getenv('MODEL_NAME', 'demo-model')

print("SDK version:", azureml.core.VERSION)

ws = Workspace.from_config()
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep = '\n')

datastore = ws.get_default_datastore()

model = Model(ws, name=model_name)

input_ds = Dataset.get_by_name(ws, dataset_name)
batch_data = DatasetConsumptionConfig("batch_dataset", input_ds, mode='mount')

output_dir = PipelineData(name='batch_output', datastore=datastore)

environment = RunConfiguration.load(runconfig).environment

parallel_run_config = ParallelRunConfig(
    source_directory=source_directory,
    entry_script='score_batch.py',
    mini_batch_size='1',
    run_invocation_timeout=180, 
    error_threshold=10,
    output_action='append_row',
    append_row_file_name='batch-predictions.txt',
    environment=environment, 
    process_count_per_node=1,
    compute_target='cpu-cluster',
    node_count=1
)

batch_step = ParallelRunStep(
    name="batch-inference-step",
    parallel_run_config=parallel_run_config,
    inputs=[batch_data],
    output=output_dir,
    allow_reuse=False,
    models=[model],
    arguments=[]
)

steps = [batch_step]

pipeline = Pipeline(workspace=ws, steps=steps)
pipeline.validate()

pipeline_run = Experiment(ws, 'batch-pipe').submit(pipeline)
pipeline_run.wait_for_completion()

#published_pipeline = pipeline.publish(pipeline_name)
#print("Published pipeline id: ", published_pipeline.id)
