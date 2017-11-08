import boto3

# create a boto3 session (should load your stored credentials automatically)
session = boto3.Session()

# create a client for interacting with dynamodb
dynamodb = session.resource('dynamodb')

table = dynamodb.create_table(
    TableName='DYNAMO_DB_RESULTS_TABLE',
    KeySchema=[
        {
            'AttributeName': 'tags',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'updated',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'tags',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'updated',
            'AttributeType': 'N'
        }

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 20,
        'WriteCapacityUnits': 5,
    }
)

table.meta.client.get_waiter(
    'table_exists'
).wait(
    TableName='DYNAMO_DB_RESULTS_TABLE'
)
