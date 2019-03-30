# -*- coding: utf-8 -*-
#
# Author: Dave Hill
# This code will trigger a lambda function

import boto3
import json

def ActivateLambdaNotifcation(deliverableMessage):
    lambdaClient = boto3.client('lambda')
    payload = {}
    payload["message"] = deliverableMessage
    response = lambdaClient.invoke(
        FunctionName='arn:aws:lambda:eu-west-1:924169754118:function:sendSNSfromChaosMonkey',
        InvocationType='RequestResponse',       # set to 'dryrun' to test permissions
        LogType='Tail',
        Payload=json.dumps(payload),            # Payload needs to be converted from String for lambda function to work
    )
    print("Sending notification to lambda")


