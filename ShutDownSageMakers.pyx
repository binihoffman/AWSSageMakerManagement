import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def call_logic():
    client = boto3.client('sagemaker')
    instances_dict = client.list_notebook_instances(MaxResults=100, StatusEquals='InService')
    print(instances_dict)
    instances = instances_dict.get('NotebookInstances')
    print(instances)
    # loop over the instances and stop the untagged ones
    for i in instances:
        stop_instance = True
        arn = i['NotebookInstanceArn']
        name = i['NotebookInstanceName']
        print('arn - ' + arn + ' name - ' + name)
        tags = client.list_tags(ResourceArn=arn).get('Tags')
        for tag in tags:
            # check if the instance is tagged for not to delete
            print('tag - ' + tag['Key'] + '---' + tag['Value'])
            if (tag['Key'] == 'AutoOff') and (tag['Value'] == 'No'):
                stop_instance = False
        if stop_instance:
            print('stopping - ' + name)
            logger.info('Stopping SakeMaker instance: {0}'.format(name))
            client.stop_notebook_instance(NotebookInstanceName=name)


def lambda_handler(event, context):
    call_logic()


if __name__ == "__main__":
    call_logic()
