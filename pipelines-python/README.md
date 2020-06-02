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
| `--dataset`           | References the default dataset by name in the AML workspace that should be used for training | 
| `--runconfig`         | Path to the runconfig that configures the training |
| `--source_directory`  | Path to the source directory containing the training code | 

Example:
```
python pipeline.py --pipeline_name training_pipeline --dataset german-credit-dataset --runconfig pipeline.runconfig --source_directory ../../src/model1/
```

