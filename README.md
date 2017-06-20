# AWS Serverless Application Model (SAM) Example
## Objective
This is example of the Amazon SAM CloudFormation Transform to deploy a simple API endpoint. This example is meant to be a deployable artifact take home from the [AWS Michigan Meetup](https://www.meetup.com/AWS-Michigan/). This example will use CloudFormation, the Serverless Application Model tranform, AWS Lambda, Swagger, and AWS Rekognition. 

## Preparation and Demonstration
Before you jump head first into SAM you need code for Lambda to run. Code for Lambda has been provided in the [lambda directory](./lambda/cats/lambda_function.py). The to run that code with API-Gateway you'll want to define your API in Swagger because configuring API Gateway by hand is tedious and you might as well document your API along the way. There's a provided [Swagger Doc](./docs/awscats.yml) as well. In this example / demo we'll use AWS CloudFormation to tie Lambda and AWS-Gateway together quickly with the SAM Transform. A CloudFormation [template](./cloudformation/cats/cats.yml) has been provided. To make things easier on you, and to aviod questions for myself, there's also some [scripts](./scripts/) provided to help ease along the deployment.

### Assumptions:
* You have an AWS Account.
* You’re using Bash.
* You have pip installed
* You're the AWS CLI installed, preferred version 1.11.108 or greater. [Help](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)
* You have configured the CLI, set up AWS IAM access credentials. [Help](http://docs.aws.amazon.com/cli/latest/reference/configure/index.html)

### Step 1: Create a S3 Bucket.
You will need a S3 bucket to work out of, we will use this bucket to upload our CloudFormation templates, our lambda code zip, and the swagger doc. Create the bucket with the following CLI command or through the console. Keep in mind that S3 bucket names are globally unique and you will have to come up with a bucket name for yourself.
```
aws s3 mb s3://sam_example_{yourName}
```

### Step 2: Clone the example Github project.
I have prepared a Github project with all of the example CloudFormation and code to get you off the ground. Clone this Github project to your local machine.

https://github.com/dejonghe/SAM-Example

### Step 3: Run the scripts.
You must run two scripts from within the Github project. Both of these scripts are to be ran from the base of the repository.

Script 1: build_lambdas.sh, this script will utilize pip to install the required packages for the lambda to the local directory, zip up the lambda function with all of the dependencies and place it in a new directory ./builds/.

```
./scripts/build_lambdas.sh
```
Script 2: s3_sync.sh, this script will sync all the necessary files to your S3 bucket. The files it syncs are the builds and cloudformation directories.

```
./scripts/s3_sync.sh -b sam_example_{yourName}
```
### Step 5: Create the CloudFormation Stack.
This is the final step in the demonstration, the following command creates and executes a change set from the template specified and sets the stack name to sam-example. The parameters come next, the AppArchive parameter is the path to the code archive within your bucket and is already configured based on the scripts ran earlier. The next parameter is the CloudToolsBucket parameter this is the name of your bucket. The Environment parameter is used to create a stage name for your API. Lastly we have the SwaggerDoc parameter this is the path to the Swagger Document and is predefined based on the scripts ran earlier. After this you must provide IAM capabilities to this CloudFormation stack because we must create an IAM role for the lambda function to run.

```
aws cloudformation deploy --template-file cloudformation/cats.yml --stack-name sam-example --parameter-overrides AppArchive=builds/cats.zip CloudToolsBucket=sam_example_{Your_Name} Environment=Dev SwaggerDoc=docs/awscats.yml --capabilities CAPABILITY_IAM
```

Wait for the CloudFormation stack to complete and then check in on the AWS Gateway, it will have a URL for you to use to hit your new API. This concludes the demonstration.
