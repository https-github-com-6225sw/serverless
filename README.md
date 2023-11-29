# serverless


## Description

Lambda Function to send email to user, track email in dynamodb, download zip file to GCP

## Getting Started

### Dependencies

* Python3
* pulumi_gcp

  

### Executing program

* get the deploy package
```
cd package
zip -r ../my_deployment_package.zip .
cd ..
zip my_deployment_package.zip lambda_function.py
```
