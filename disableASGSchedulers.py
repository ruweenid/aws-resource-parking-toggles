import boto3
import sys

def update_scheduled_actions(asg_name, desired_count):
    client = boto3.client('autoscaling')

    # Retrieve the scheduled actions for the specified Auto Scaling Group
    response = client.describe_scheduled_actions(AutoScalingGroupName=asg_name)

    for action in response['ScheduledUpdateGroupActions']:
        # Check if the scheduled action name contains 'stop'
        if 'stop' in action['ScheduledActionName'].lower():

            print(f"Updating Scheduled Action - {action['ScheduledActionName']}")
            # Update the desired count, max, and min values with the current desired count
            client.put_scheduled_update_group_action(
                AutoScalingGroupName=asg_name,
                ScheduledActionName=action['ScheduledActionName'],
                MinSize=desired_count,
                MaxSize=desired_count,
                DesiredCapacity=desired_count,
                Recurrence='0 19 * * MON-FRI'
            )

def main(environment):
    client = boto3.client('autoscaling')

    # Retrieve all Auto Scaling Groups using pagination
    paginator = client.get_paginator('describe_auto_scaling_groups')
    response_iterator = paginator.paginate()

    for response in response_iterator:
        for group in response['AutoScalingGroups']:
            # Check if the Auto Scaling Group name contains the specified environment
            if environment in group['AutoScalingGroupName']:
                print(f"AutoScaling Group Name = {group['AutoScalingGroupName']}")
                asg_name = group['AutoScalingGroupName']
                desired_count = group['DesiredCapacity']
                update_scheduled_actions(asg_name, desired_count)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the environment (qa or dev) as an argument.")
        sys.exit(1)
    environment = sys.argv[1]
    main(environment)