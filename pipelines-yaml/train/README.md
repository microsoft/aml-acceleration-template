# Instructions

Attach the folder with the pipeline to the AML workspace (run this command from this folder):
```
az ml folder attach -g aml-demo -w aml-demo
```

Execute pipeline:
```
az ml run submit-pipeline -n pipeline-test-exp -y pipeline.yml
```
