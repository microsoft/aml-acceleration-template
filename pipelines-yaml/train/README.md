# Instructions

Attach the whole repo to the AML workspace (run this command from the repo's root folder):
```
az ml folder attach -g aml-demo -w aml-demo
```

Execute pipeline:
```
az ml run submit-pipeline -n pipeline-test-exp -y pipeline.yml
```
