import boto3

client = boto3.client('sagemaker')
response = client.describe_notebook_instance(NotebookInstanceName='DSS-Instance-DssXsightModelTest-Vikings-v1-0-20')
for keys, values in response.items():
    print (keys)
    print (values)