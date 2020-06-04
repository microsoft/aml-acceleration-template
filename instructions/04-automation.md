### Create New Project

1. Sign in to [Azure DevOps](http://dev.azure.com)
1. Select **Create project**
1. Provide Project Name: `aml-acceleration-template` and select **Create**
    
###  Import Quickstart code from a Github Repo

**TODO**: Use GitHub as main repo, rather than importing it?!

1. Within the new project:
   1. Select **Repos** from left navigation bar 
   1. Select **Import** from the content section 
1. Provide the Github URL of your cloned aml_accelarator template instance and select **Import**. 

### Create new Service Connection

1. From the left navigation select **Project settings** and then select **Service connections**
1. Select **New service connection** and then select **Azure Resource Manager**
1. Provide the following information in the `Add an Azure Resource Manager service connection` dialog box and then select **Ok**:
   1. Connection name: `azure_service_connection_name`
   1. Subscription: Select the Azure subscription to use
   1. Resource Group: This value should match the value you provided in the `automation/deploy-ml-train-pipeline.yml` file

### Update the build YAML file

1. Select and open the `automation/deploy-ml-train-pipeline.yml` file
1. Select **Edit** and update the following variables: 
  ```
  resourcegroup
  workspace
  aml_compute_target
  pipeline_name
  dataset
  dataset_test
  ```
1. Select **Commit** to save your changes. 

### Create/Verify Dataset in AML 

1. Follow instruction on [Create Dataset in AML from Training Page](https://github.com/microsoft/aml-acceleration-template/blob/master/instructions/01-training.md)

### Setup Build Pipeline

1. From left navigation select **Pipelines, Builds** and then select **New pipeline**
1. Select **Azure Repos Git** as your code repository
1. Select **aml_accelarator** as your repository
1. Review the YAML file, the build pipeline has four key steps:
    * Attach folder to workspace
    * Create the AML Compute target
    * Create pipeline for model training
    * Execute tests for running the training pipeline using a small training dataset (functional test)
    * Publish the test results

### Run the Build Pipeline

1. Select **Run** to start running your build pipeline
1. Monitor the build run. 
