# -*- coding: utf-8 -*-
#
# Author: Dave Hill
# This is the code the lamdba function is running for reference when reviewing this project.


import json
import boto3


def lambda_handler(event, context):
    TARGET_ARN = "arn:aws:sns:eu-west-1:924169754118:chaosMonkey-notifications"

    snsclient = boto3.client('sns')

    message = event["message"]

    print(message)

    response = snsclient.publish(
        TargetArn=TARGET_ARN,
        Message=message
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Hope this works')
    }
