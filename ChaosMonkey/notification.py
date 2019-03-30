# -*- coding: utf-8 -*-
#
# Author: Dave Hill
# This code will trigger a SNS notification

import boto3

# CONSTANTS
TARGET_ARN = "arn:aws:sns:eu-west-1:924169754118:chaosMonkey-notifications"

def sendSNSNotification(deliverableMessage):
    snsClient = boto3.client('sns')
    response = snsClient.publish(
        TargetArn=TARGET_ARN,
        Message=deliverableMessage
    )
    print("Sending notification to "+TARGET_ARN)


