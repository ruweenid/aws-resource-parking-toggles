import boto3
import sys

def set_autostart_autostop_tags(cluster_name, value):
    rds_client = boto3.client('rds')

    try:
        # Get the current tags for the cluster
        response = rds_client.list_tags_for_resource(ResourceName=cluster_name)
        current_tags = response['TagList']

        # Update the AutoStart and AutoStop tags to False
        updated_tags = []
        for tag in current_tags:
            if tag['Key'] == 'AutoStart' or tag['Key'] == 'AutoStop':
                tag['Value'] = value
            updated_tags.append(tag)

        # Apply the updated tags to the cluster
        rds_client.add_tags_to_resource(ResourceName=cluster_name, Tags=updated_tags)
        print(f"AutoStart and AutoStop tags set to {value} for cluster: {cluster_name}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    lambda_env = sys.argv[1]
    action = sys.argv[2]

    if action.lower() == 'true':
        value = 'true'
    elif action.lower() == 'false':
        value = 'false'
    else:
        print("Invalid action. Please specify either 'true' or 'false'.")
        sys.exit(1)

    if lambda_env.lower() == 'dev':
        cluster_name = 'arn:aws:rds:eu-west-2:362392363900:cluster:dev-db-1-cluster'
    elif lambda_env.lower() == 'qa':
        cluster_name = 'arn:aws:rds:eu-west-2:362392363900:cluster:qa-db-1-cluster-cluster'
    else:
        print("Invalid environment. Please specify either 'dev' or 'qa'.")
        sys.exit(1)


    set_autostart_autostop_tags(cluster_name, value)


# arn:aws:rds:eu-west-2:362392363900:cluster:dev-db-1-cluster
# arn:aws:rds:eu-west-2:362392363900:cluster:qa-db-1-cluster-cluster