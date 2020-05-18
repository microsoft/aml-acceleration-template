"""
This pipeline.py script will be run by the CI/CD tool to publish out a new pipeline based on changes to the training script.
"""
import argparse
import os
from pprint import PrettyPrinter

import azureml.core
from azureml.contrib.notebook import NotebookRunnerStep, NotebookRunConfig
from azureml.core import (Dataset, Datastore, Experiment, RunConfiguration,
                          Workspace)
from azureml.core.authentication import AzureCliAuthentication
from azureml.core.compute import AmlCompute, ComputeTarget
from azureml.pipeline.core import Pipeline, PipelineData

print("Pipeline SDK-specific imports completed")
# Check core SDK version number
print("Azure ML SDK version:", azureml.core.VERSION)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser("create_notebook_pipeline")
    parser.add_argument("--model_name",
                        type=str,
                        help="model name",
                        required=True)
    parser.add_argument("--build_number",
                        type=str,
                        help="build number",
                        required=False)
    parser.add_argument("--image_name",
                        type=str,
                        help="image name",
                        required=True)
    parser.add_argument("--path", type=str, help="path", required=True)
    parser.add_argument("--dataset", type=str, help="dataset", required=True)
    parser.add_argument("--dataset_mountpath",
                        type=str,
                        help="dataset_mountpath",
                        required=True)
    parser.add_argument("--runconfig",
                        type=str,
                        help="runconfig",
                        required=True)
    parser.add_argument("--source_directory",
                        type=str,
                        help="source_directory",
                        required=True)
    parser.add_argument('--notebook_name',
                        type=str,
                        help="The filename of the notebook to be run in relation to source directory.")

    args = parser.parse_args()
    print("---------------------")
    print("Arguments passed:")
    PrettyPrinter().pprint(args.__dict__)

    return args


def get_workspace(config_path: str) -> azureml.core.Workspace:
    print('Creating AzureCliAuthentication...')
    cli_auth = AzureCliAuthentication()
    print('Done creating AzureCliAuthentication!')

    print('Connecting to Azure ML Workspace')
    ws = Workspace.from_config(path=config_path, auth=cli_auth)
    print("Azure ML Workspace Connected:",
          '    Workspace name: ' + ws.name,
          '    Azure region: ' + ws.location,
          '    Subscription id: ' + ws.subscription_id,
          '    Resource group: ' + ws.resource_group,
          sep='\n')

    return ws


def args_to_dicts(arguments: list) -> dict:
    it = iter(arguments)
    return dict(zip(it, it))

def load_runconfig(runconfig: str, source_directory: str,
                   notebook_name: str) -> azureml.contrib.notebook.NotebookRunConfig:
    print('--------------------------', 
          "Loading Run Configuration", 
          sep="\n")
    rc = RunConfiguration.load(runconfig)
    nb_runconfig = NotebookRunConfig(source_directory=source_directory,
                                     notebook=notebook_name,
                                     parameters=args_to_dicts(rc.arguments),
                                     run_config=rc)

    print('--------------------------')
    return nb_runconfig


def load_dataset(dataset: str, mount_path: str, ws: azureml.core.Workspace) -> azureml.core.Dataset:
    print("Loading dataset")
    input_ds = Dataset.get_by_name(ws, dataset)
    training_data = input_ds.as_named_input('training_dataset').as_mount(
        path_on_compute=mount_path)

    return training_data


def main():

    #  Parse Command Line Arguments
    args = parse_arguments()

    # Connect to Workspace
    ws = get_workspace(args.path)

    # Load RunConfig
    runconfig = load_runconfig(args.runconfig, args.source_directory,
                               args.notebook_name)

    # Get Dataset
    training_data = load_dataset(args.dataset, args.dataset_mountpath, ws)

    # Create NotebookRunnerStep
    train_step = NotebookRunnerStep(name="train-step",
                                    notebook_run_config=runconfig,
                                    compute_target=runconfig.run_config.target,
                                    inputs=[training_data],
                                    allow_reuse=False)

    print('Creating and validating pipeline...', )

    pipeline = Pipeline(workspace=ws, steps=[train_step])
    pipeline.validate()

    print("  Validation complete!")

    print("Publishing Pipeline... ", )
    published_pipeline = pipeline.publish(args.model_name)
    print("Pipeline published. ID: {0}".format(published_pipeline.id))


if __name__ == "__main__":
    main()
