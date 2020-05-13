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

parser.add_argument("--dataset", type=str, help="dataset", dest="dataset", required=True)
parser.add_argument("--dataset_mountpath", type=str, help="dataset_mountpath", dest="dataset_mountpath", required=True)
parser.add_argument("--runconfig", type=str, help="runconfig", dest="runconfig", required=True)
args = parser.parse_args()

#dataset_name =  os.getenv('DATASET', 'german-credit-filedataset')
#dataset_mountpath = os.getenv('DATASET_MOUNTPATH', '/data')
#source_directory = os.getenv('SOURCE_DIRECTORY', '../../src/model1/')
#runconfig = os.getenv('RUNCONFIG', 'pipeline.runconfig')


print("Argument 1: %s" % args.aml_compute_target)
print("Argument 2: %s" % args.model_name)
print("Argument 3: %s" % args.build_number)
print("Argument 4: %s" % args.image_name)
print("Argument 5: %s" % args.path)
print("Argument 6: %s" % args.dataset)
print("Argument 7: %s" % args.dataset_mountpath)
print("Argument 8: %s" % args.runconfig)

print('creating AzureCliAuthentication...')
cli_auth = AzureCliAuthentication()
print('done creating AzureCliAuthentication!')

print('get workspace...')
ws = Workspace.from_config(path=args.path, auth=cli_auth)
print('done getting workspace!')

print("looking for existing compute target.")
aml_compute = AmlCompute(ws, args.aml_compute_target)
print("found existing compute target.")


scripts_folder = 'scripts'
def_blob_store = ws.get_default_datastore()

train_output = PipelineData('train_output', datastore=def_blob_store)
print("train_output PipelineData object created")


ws = Workspace.from_config()
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep = '\n')

print('--------------------------')
print(runconfig)
base_dir= 'pipelines-python/train/'
filepath = os.path.join(base_dir, 'pipeline.runconfig')
print(filepath)

runconfig = RunConfiguration.load(runconfig)

input_ds = Dataset.get_by_name(ws, dataset_name)
training_data = input_ds.as_named_input('training_dataset').as_mount(path_on_compute=dataset_mountpath)


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

#pipeline_run = Experiment(ws, 'train-pipe').submit(pipeline)
#pipeline_run.wait_for_completion()

published_pipeline = pipeline.publish(pipeline_name)
print("Published pipeline id: ", published_pipeline.id)
