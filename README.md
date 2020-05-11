# Azure Machine Learning Acceleration Template

<!-- 
Guidelines on README format: https://review.docs.microsoft.com/help/onboard/admin/samples/concepts/readme-template?branch=master

Guidance on onboarding samples to docs.microsoft.com/samples: https://review.docs.microsoft.com/help/onboard/admin/samples/process/onboarding?branch=master

Taxonomies for products and languages: https://review.docs.microsoft.com/new-hope/information-architecture/metadata/taxonomies?branch=master
-->

This repo features a Azure Machine Learning (AML) Acceleration template which enables you to quickly onboard your existing Machine Learning code to AML. The template enables a smooth ML development process between your local machine and the Azure Cloud. Furthermore, it includes simple examples for running your model training and batch inferecing as [Machine Learning Pipelines](https://docs.microsoft.com/en-us/azure/machine-learning/concept-ml-pipelines) for automation.

If you want to follow a structured approach to use this repo, start with [migrating your first workload to AML](instructions/README.md) and walk through the separate sections.

## Contents

This repo follows a pre-defined structure for storing your model code, pipelines, etc.

| File/folder       | Description                                |
|-------------------|--------------------------------------------|
| `instructions\`   | A step-by-step guide on how to onboard your first workload to AML. |
| `sample-data\`   | Some small sample data used for the template example. |
| `src\`             | Model code and other required code assets. |
| `src\model1`     | A full end-to-end example for training, real-time and batch inferencing and automation. |
| `pipelines-yaml\`  | A set of [YAML-based ML pipelines](https://docs.microsoft.com/en-us/azure/machine-learning/reference-pipeline-yaml).      |
| `pipelines-py\`    | A set of Python-based ML pipelines.             |


## Prerequisites

This repo requires a few prerequisites to be installed:

* Azure Machine Learning service provisioned - follow [this tutorial](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace#create-a-workspace)
* Docker installed - see [here](https://docs.docker.com/get-docker/)
* Azure CLI installed - see [here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
* Azure Machine Learning CLI extension installed - see [here](https://docs.microsoft.com/en-us/azure/machine-learning/reference-azure-machine-learning-cli)

A full list of prerequisites and introductions is documented [here](instructions/00-prerequisites.md).

## Setup

If you want to follow a structured approach to use this repo, start with [migrating your first workload to AML](instructions/README.md) and walk through the separate sections.

## Authors

* Clemens Siebler, AI Technical Specialist GBB EMEA
* Erik Zwiefel, AI Principal Technical Specialist GBB Americas
* Alan Weaver, AI Senior Technical Specialist GBB EMEA
* Alexander Zeltov, AI Principal Technical Specialist GBB Americas

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
