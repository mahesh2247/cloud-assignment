# montycloud-assignmentapp


This project was based on an assignment.

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. 

It includes the following files and folders.

- src - Code for the application's Lambda function.
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.


## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

After running the above commands you will get a API endpoint 

## To Run your application on Postman

* Copy the API Gateway link with key `ImageUploadApi` recieved after succesfully deploying SAM
* Open Postman , enter the API Gateway URL in the URL box , choose the POST Method
* Choose the 'Body' Tab below and select the binary option on the radio button
* Choose any JPEG Image and click on Send
* After processesing , you will see API response which contains JSON with the keys message <relevant_message> and file_name <random_uuid>.jpg
* Check your S3 bucket from your Cloudformation stack and you will see antoher folder for thumbnail which is a thumbnail for the same image which was uploaded along with an image folder which will contain the image you just uploaded.
* Copy the API Gateway link with key `FileDownloadApi` recieved when you first deployed SAM
* In Postman , provide the `file_name` as seen on the s3 bucket or from the response obtained from the `ImageUploadApi` under `file_name`
* Use the GET Method and click on Send. You should have now recieved the file on your local system.
