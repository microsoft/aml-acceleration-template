# ML Pipelines

## Executing training in a ML Pipeline

1. Execute training in a ML Pipeline 
    * Open the terminal and navigate to the [`pipelines/train-pipeline-yaml`](../pipelines/train-pipeline-yaml/) folder
    * Open `pipeline.yml` in your editor and adapt the necessary fields, which are most likely:
        * `default_compute` - point to the AML Compute cluster created earlier
        * `dataset_name` - point to your dataset registerd earlier (this time by specifying the name)
        * `script_name` - point to your training script
        * `arguments` - adapt to point to the data path and add further arguments (similar to the training stage)
    * (Optional) Open `pipeline.runconfig` and adapt if need (if you kept the defaults, there won't be a need for it)
    * From the command line, you can now run the training in a pipeline:
    ```
    az ml run submit-pipeline -n training-pipeline-exp -y pipeline.yml
    ```

1. Once the pipeline is working, you can publish it as a RESTful endpoint from which it can be triggered
    * Publish pipeline as RESTful endpoint (you will see its `id` in the response):
    ```
    az ml pipeline create -n training-pipeline -y pipeline.yml
    ```
    * Run pipeline using its `id`:
    ```
    az ml run submit-pipeline -n training-pipeline-exp -i b740c140-2a70-4dac-9cc8-8d6c67f65619
    ```

## Executing batch inferencing in a ML Pipeline

1. TODO: To be written


Great, we got our training and batch scoring running in a ML pipeline. Let's move on to the [next section](04-automation.md) and automate it.