import os
import azureml.core
from azureml.core import Workspace, Experiment, Datastore, Dataset, RunConfiguration

from azureml.pipeline.core import Pipeline
from azureml.pipeline.steps import PythonScriptStep

print("Pipeline SDK-specific imports completed")
# Check core SDK version number
print("Azure ML SDK version:", azureml.core.VERSION)

parser = argparse.ArgumentParser("pipelines_master")
parser.add_argument("--aml_compute_target", type=str, help="compute target name", dest="aml_compute_target", required=True)
parser.add_argument("--model_name", type=str, help="model name", dest="model_name", required=True)
parser.add_argument("--build_number", type=str, help="build number", dest="build_number", required=True)
parser.add_argument("--image_name", type=str, help="image name", dest="image_name", required=True)
parser.add_argument("--path", type=str, help="path", dest="path", required=True)
args = parser.parse_args()

print("Argument 1: %s" % args.aml_compute_target)
print("Argument 2: %s" % args.model_name)
print("Argument 3: %s" % args.build_number)
print("Argument 4: %s" % args.image_name)
print("Argument 5: %s" % args.path)

print('creating AzureCliAuthentication...')
cli_auth = AzureCliAuthentication()
print('done creating AzureCliAuthentication!')

print('get workspace...')
ws = Workspace.from_config(path=args.path, auth=cli_auth)
print('done getting workspace!')

print("looking for existing compute target.")
aml_compute = AmlCompute(ws, args.aml_compute_target)
print("found existing compute target.")

# Create a new runconfig object
run_amlcompute = RunConfiguration()

# Use the cpu_cluster you created above. 
run_amlcompute.target = args.aml_compute_target

# Enable Docker
run_amlcompute.environment.docker.enabled = True

# Set Docker base image to the default CPU-based image
run_amlcompute.environment.docker.base_image = DEFAULT_CPU_IMAGE

# Use conda_dependencies.yml to create a conda environment in the Docker image for execution
run_amlcompute.environment.python.user_managed_dependencies = False

# Auto-prepare the Docker image when used for execution (if it is not already prepared)
run_amlcompute.auto_prepare_environment = True

# Specify CondaDependencies obj, add necessary packages
run_amlcompute.environment.python.conda_dependencies = CondaDependencies.create(pip_packages=[
    'numpy',
    'pandas',
    'tensorflow==2.0.0',
    'keras==2.3.1',
    'azureml-sdk',
    'azureml-dataprep[pandas]'
])

scripts_folder = 'scripts'
def_blob_store = ws.get_default_datastore()

train_output = PipelineData('train_output', datastore=def_blob_store)
print("train_output PipelineData object created")

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
