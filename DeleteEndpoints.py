import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def call_logic():
    client = boto3.client('sagemaker')
    # create_endpoint_config_test(client)
    end_points_list = client.list_endpoints()
    # get details of all the existing endpoints
    ep = end_points_list.get('Endpoints')
    logger.info('SageMaker endpoints list: {0}'.format(ep))
    print(ep)
    # loop over the endpoints and delete the untagged ones
    for i in ep:
        delete_ep = True
        if (i['EndpointStatus'] == 'InService'):
            arn = i['EndpointArn']
            name = i['EndpointName']
            tags = client.list_tags(ResourceArn=arn).get('Tags')
            for tag in tags:
                # check if the endpoint is tagged for not to delete
                if ((tag['Key'] == 'AutoOff') and (tag['Value'] == 'No')):
                    delete_ep = False
            if (delete_ep):
                print('delete - ' + name)
                logger.info('Deleting SakeMaker endpoint: {0}'.format(name))
                client.delete_endpoint(EndpointName=name)


def lambda_handler(event, context):
    call_logic()



def create_endpoint_config_test(client):
    response = client.create_endpoint(
        EndpointName='testendpoint2',
        EndpointConfigName='xgboost-2018-07-08-15-27-58-021',
        Tags=[
            {
                'Key': 'test',
                'Value': 'test'
            },
        ]
    )

if __name__ == "__main__":
    call_logic()


