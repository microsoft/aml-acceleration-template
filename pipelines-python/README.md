# Instructions

From within the directory of each pipeline, you can run it via:

```
python pipeline.py --pipeline_name training_pipeline --dataset german-credit-dataset --dataset_mountpath /data --runconfig pipeline.runconfig --source_directory ../../src/model1/
```

The pipelines have different parameters which can be defined via environment variables or script arguments.

## `train` pipeline

The `train` pipeline file accepts command line arguments for creating the pipeline.

<!--TODO: Finish Table with Descriptions -->
| Argument              | Description |
|:--------------------  | ------------|
| `--model_name`        | The name of the model to be registered |
| `--build_number`      | (Optional) The build number |
| `--dataset`           | References the dataset in the AML workspace that should be mounted for training | 
| `--dataset_mountpath` | Path on the AML Compute Cluster where the dataset should be mounted to |
| `--runconfig`         | Runconfig that configures the training |
| `--source_directory`  | Source directory for the training code | 


## `batch-inference` pipeline

| ENV variable | Default | Description |
|-------|--------|------|
| `DATASET` | `german-credit-filedataset` | References the dataset in the AML workspace that is used for batch inferencing | 
| `SOURCE_DIRECTORY` | `../../src/model1/` | Source directory for the batch inferencing code | 
| `RUNCONFIG` | `pipeline.runconfig` | Runconfig that configures the batch inferencing |
| `MODEL_NAME` | `demo-model` | Model name from the AML workspace that should be used for batch inferencing |
