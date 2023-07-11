import boto3
import sys

def toggle_event_bridge_triggers(lambda_function_arn, enable):
    client = boto3.client('events')
    
    try:
        response = client.list_rule_names_by_target(TargetArn=lambda_function_arn)
        rule_names = response['RuleNames']
        print(rule_names)
        
        for rule_name in rule_names:
            response = client.disable_rule(Name=rule_name) if not enable else client.enable_rule(Name=rule_name)
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                print(f"Failed to toggle EventBridge trigger for rule: {rule_name}")

        print(f"EventBridge triggers for Lambda function '{lambda_function_arn}' have been {'enabled' if enable else 'disabled'}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    lambda_env = sys.argv[1]
    action = sys.argv[2]

    if action.lower() == 'enable':
        enable_triggers = True
    elif action.lower() == 'disable':
        enable_triggers = False
    else:
        print("Invalid action. Please specify either 'enable' or 'disable'.")
        sys.exit(1)

    if lambda_env.lower() == 'dev':
        lambda_function_arn = 'arn:aws:lambda:eu-west-2:362392363900:function:dev-devops-AutoStopECSServiceLambda'
    elif lambda_env.lower() == 'qa':
        lambda_function_arn = 'arn:aws:lambda:eu-west-2:362392363900:function:qa-devops-AutoStopECSServiceLambda'
    else:
        print("Invalid environment. Please specify either 'dev' or 'qa'.")
        sys.exit(1)

    toggle_event_bridge_triggers(lambda_function_arn, enable_triggers)
