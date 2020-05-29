# Instructions

From within the directory of each pipeline, you can run it via:

```
python pipeline.py <arguments>
```

## `train` pipeline

The `train` pipeline deployment accepts command line arguments for creating the pipeline:

| Argument              | Description |
|:--------------------  | ------------|
| `--pipeline_name`        | Name of the pipeline that will be deployed |
| `--build_number`      | (Optional) The build number |
| `--dataset`           | References the dataset by name in the AML workspace that should be mounted for training | 
| `--dataset_mountpath` | Path on the AML Compute Cluster where the dataset should be mounted to |
| `--runconfig`         | Path to the runconfig that configures the training |
| `--source_directory`  | Path to the source directory containing the training code | 

Example:
```
python pipeline.py --pipeline_name training_pipeline --dataset german-credit-filedataset --dataset_mountpath /data --runconfig pipeline.runconfig --source_directory ../../src/model1/
```

