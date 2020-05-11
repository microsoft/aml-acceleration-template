# Training

1. Create a new Git repository from this repo and open it
    * Open [this template repo](https://github.com/microsoft/aml-acceleration-template) in a new browser tab and click `Use this template` and create a new repo from it
    * In vscode, open `Terminal` by selecting `View -> Terminal` to open the terminal
    * Clone your newly created repo:
    ```
        git clone <URL to your repo>
    ```

1. Copy your Machine Learning code into the repository
    * Copy your existing Machine Learning code to the [`src/model1/`](../src/model1/) directory
    * If you already have a `train.py` or `score.py`, just rename the existing examples for later use as reference
    * If you are converting an existing `ipynb` notebook, you can easily convert it to a python script using these commands:
        ```
        pip install nbconvert
        jupyter nbconvert --to script training_script.ipynb 
        ```
    * However, be aware to follow the `train.py` outline with parameters for inputting the source for data path

1. Adapt Conda environment
    * *Case 1* - You are using `conda env`
        * If you do not have an existing Conda env yaml file, run `conda env export > temp.yml` from the correct Conda env
        * Move your existing Conda environmnent into [`aml_config/train-conda.yml`](../src/model1/aml_config/train-conda.yml) (make sure to keep the `azureml-*` specific dependencies!)
    * *Case 2* - You are using a `pip`
        * If you do not have an existing `requirements.txt`, run `pip freeze > requirements.txt`
        * Move your content from your `requirements.txt` into [`aml_config/train-conda.yml`](../src/model1/aml_config/train-conda.yml) (make sure to keep the `azureml-*` specific dependencies!)
    * *Case 3* - It's more complicated
        * Make a good assumption what your dependencies are and put them into [`aml_config/train-conda.yml`](../src/model1/aml_config/train-conda.yml) (make sure to keep the `azureml-*` specific dependencies!)

1. Update your training code to serialize your model
    * Update your training code to write out the model to an `outputs/` folder
    * Either directly leverage your ML framework or use e.g., `joblib`. Adapt your code to something like this:
    ```python
    import joblib, os

    output_dir = './outputs/'
    os.makedirs(output_dir, exist_ok=True)
    joblib.dump(value=clf, filename=os.path.join(output_dir, "model.pkl"))
    ```

1. Adapt local runconfig for local training
    * Open [`aml_config/train-local.runconfig`](../src/model1/aml_config/train-local.runconfig) in your editor
    * Update the `script` parameter to your entry script (default is `train.py`)
    * Update the `arguments` parameter and point your data path parameter to `/data` and adapt other parameters
    * Under the `environment -> docker` section, change `arguments: [-v, /full/path/to/sample-data:/data]` to the full path to your data folder on your disk
    * If you use the Compute Instance in Azure, copy the files into the instance first and then reference the local path

1. Open `Terminal` in VSCode and run the training against the local instance
    * Select `View -> Terminal` to open the terminal
    * Switch to the directory with the code:
    ```
    cd path/to/src/model1/
    ```
    * Attach the current folder to the AML workspace:
    ```
    az ml folder attach -g <your-resource-group> -w <your-workspace-name>
    # Default will be az ml folder attach -g aml-demo -w aml-demo
    ```
    * Submit the `train-local.runconfig` against the local host (either Compute Instance or your local Docker environment)
    ```
    az ml run submit-script -c train-local -e aml-poc-local
    ```
    * If it runs through, perfect - if not, follow the error message and adapt data path, conda env, etc. until it works

1. Create Dataset in AML with data
    * TODO: We need to add more details on this
    * TODO: New container or use existing default workspace container?
    * *Option 1* - Using CLI:
        * Execute the following commands in the terminal:
        ```
        az storage account keys list -g <your-resource-group> -n <storage-account-name>
        az storage container create -n <container-name> --account-name <storage-account-name>
        az storage blob upload -f <<filename.csv>> -c <container-name> -n file_name.csv --account-name <storage-account-name>
        ```
    * *Option 2* - Using Azure Storage Explorer:
        * Install [Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/)
        * Upload data to the default `workspaceblobstore` under a new folder
    * In the Azure ML UI, register this folder as a new `File Dataset` under `Datasets`, clock `+ Create dataset`, then select `From datastore`

1. Provision Compute cluster in Azure Machine Learning
    * Open [Azure Machine Learning Studio UI](https://ml.azure.com)
    * Navigate to `Compute --> Compute clusters`
    * Select `+ New`
    * Set the `Compute name` to `cpu-cluster`
    * Select a `Virtual Machine type`
    * Set `Minimum number of nodes` to 0
    * Set `Maximum number of nodes` to 1
    * Set `Idle seconds before scale down` to e.g., 7200 (this will keep the cluster up for 2 hours, hence avoids startup times)
    * Hit `Create`

1. Adapt AML Compute runconfig
    * Open [`aml_config/train-local.runconfig`](../src/model1/aml_config/train-amlcompute.runconfig) in your editor
    * Update the `script` parameter to your entry script
    * Update the `arguments` parameter and point your data path parameter to `/data` and adapt other parameters
    * Update the `target` section and point it to the name of your newly created Compute cluster (default `cpu-cluster`)
    * Find out your dataset's `id` using the command line:
    ```
    az ml dataset list
    ```
    * Under the `data` section, replace `id` with your dataset's id:
    ```yaml
    data:
        mydataset:
            dataLocation:
            dataset:
                id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx # replace with your dataset's id
            ...
            pathOnCompute: /data # Where your data is mounted to
    ```

1. Submit the training against the AML Compute Cluster
    * Submit the `train-amlcompute.runconfig` against the AML Compute Cluster
    ```
    az ml run submit-script -c train-amlcompute -e aml-poc-compute -t run.json
    ```

1. Register model with metadata
    ```
    az ml model register -n demo-model --asset-path outputs/model.pkl -f run.json \
      --tag key1=value1 --tag key2=value2 --property prop1=value1 --property prop2=value2
    ```

Great, you have now trained your Machine Learning on Azure using the power of the cloud. Let's move to the [next section](02-inferencing.md) where we look into moving the inferencing code to Azure.