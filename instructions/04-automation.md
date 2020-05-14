### Create New Project

1. Sign in to [Azure DevOps](http://dev.azure.com)

2. Select **Create project**

3. Provide Project Name: `aml-acceleration-template` and select **Create**

    
###  Import Quickstart code from a Github Repo

1. Within the new project:

   a. Select **Repos** from left navigation bar
   
   b. Select **Import** from the content section
   
   
2. Provide the Github URL of your cloned aml_accelarator template instance and select **Import**. 


### Update the build YAML file

1. Select and open the `automation/deploy-ml-train-pipeline.yml` file

2. Select **Edit** and update the following variables: `resourcegroup`, and `workspace`. 

3. Select **Commit** to save your changes.

  
### Create new Service Connection

1. From the left navigation select **Project settings** and then select **Service connections**

2. Select **New service connection** and then select **Azure Resource Manager**

3. Provide the following information in the `Add an Azure Resource Manager service connection` dialog box and then select **Ok**:
 
   a. Connection name: `aml_accelarator_svc_conn`
   
   b. Subscription: Select the Azure subscription to use
   
   c. Resource Group: This value should match the value you provided in the `automation/deploy-ml-train-pipeline.yml` file

### Create/Verify Dataset in AML 

1. Follow instruction on [Create Dataset in AML from Training Page](https://github.com/microsoft/aml-acceleration-template/blob/master/instructions/01-training.md)

### Setup Build Pipeline

1. From left navigation select **Pipelines, Builds** and then select **New pipeline**
    
2. Select **Azure Repos Git** as your code repository

3. Select **aml_accelarator** as your repository

4. Review the YAML file

    The build pipeline has four key steps:
    
    a. Attach folder to workspace and experiment. 
    
    b. Create the AML Compute target to run your master pipeline for model training and model evaluation.
    
    c. Run the master pipeline. 
    
    d. Publish the build artifacts. 

### Run the Build Pipeline

1. Select **Run** to start running your build pipeline

2. Monitor the build run. 
