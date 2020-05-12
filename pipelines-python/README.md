# Instructions

From within the directory of each pipeline, you can run it via:

```
python pipeline.py
```

The pipelines have different parameters which can be defined via environment variables.


## `train` pipeline


| ENV variable | Default | Description |
|-------|--------|------|
| `DATASET` | `german-credit-filedataset` | References the dataset in the AML workspace that should be mounted for training | 
| `DATASET_MOUNTPATH` | `/data` | Path on the AML Compute Cluster where the dataset should be mounted to |
| `SOURCE_DIRECTORY` | `../../src/model1/` | Source directory for the training code | 
| `RUNCONFIG` | `pipeline.runconfig` | Runconfig that configures the training |


## `batch-inference` pipeline

| ENV variable | Default | Description |
|-------|--------|------|
| `DATASET` | `german-credit-filedataset` | References the dataset in the AML workspace that is used for batch inferencing | 
| `SOURCE_DIRECTORY` | `../../src/model1/` | Source directory for the batch inferencing code | 
| `RUNCONFIG` | `pipeline.runconfig` | Runconfig that configures the batch inferencing |
| `MODEL_NAME` | `demo-model` | Model name from the AML workspace that should be used for batch inferencing |
