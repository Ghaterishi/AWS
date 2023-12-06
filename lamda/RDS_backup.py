import boto3
from datetime import datetime

def lambda_handler(event, context):
    # Replace 'YourDBInstanceIdentifier' with the actual RDS instance identifier
    db_instance_identifier = 'REPLACEWITHDATABSENAME'
    
    rds = boto3.client('rds')
    
    try:
        # Create a snapshot of the RDS instance with a timestamp in the snapshot identifier
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        snapshot_identifier = f'{db_instance_identifier}-snapshot-{timestamp}'
        
        response = rds.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_identifier,
            DBInstanceIdentifier=db_instance_identifier
        )
        
        print(f"Snapshot {snapshot_identifier} created successfully: {response['DBSnapshot']['DBSnapshotArn']}")
        
        return {
            'statusCode': 200,
            'body': f'Snapshot {snapshot_identifier} created successfully!'
        }
    
    except Exception as e:
        print(f"Error creating snapshot: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error creating snapshot: {str(e)}'
        }
