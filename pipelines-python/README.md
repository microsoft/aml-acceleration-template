# Instructions

From within the directory of each pipeline, you can run it via:

```
python pipeline.py
```

The pipelines have different parameters which can be defined via environment variables or script arguments.


## `train` pipeline

The `train` pipeline file accepts command line arguments for creating the pipeline.

<!--TODO: Finish Table with Descriptions -->
| Argument              | Description |
|:--------------------  | ------------|
| `--model_name`        | The name of the model to be registered |
| `--build_number`      | |
| `--image_name`        | |
| `--path`              | |
| `--dataset`           | References the dataset in the AML workspace that should be mounted for training | 
| `--dataset_mountpath` | Path on the AML Compute Cluster where the dataset should be mounted to. |
| `--runconfig`         | Runconfig that configures the training |
| `--source_directory`  | Source directory for the training code | 


## `train-notebook` pipeline

The train notebook pipeline will create pipeline that executes a Jupyter Notebook using [`azureml.contrib.notebook.NotebookRunnerStep`](https://docs.microsoft.com/en-us/python/api/azureml-contrib-notebook/azureml.contrib.notebook.notebookrunnerstep?view=azure-ml-py)


## `batch-inference` pipeline

| ENV variable | Default | Description |
|-------|--------|------|
| `DATASET` | `german-credit-filedataset` | References the dataset in the AML workspace that is used for batch inferencing | 
| `SOURCE_DIRECTORY` | `../../src/model1/` | Source directory for the batch inferencing code | 
| `RUNCONFIG` | `pipeline.runconfig` | Runconfig that configures the batch inferencing |
| `MODEL_NAME` | `demo-model` | Model name from the AML workspace that should be used for batch inferencing |
