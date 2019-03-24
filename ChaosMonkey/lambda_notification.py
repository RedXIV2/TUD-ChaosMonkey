# -*- coding: utf-8 -*-
#
# Author: Dave Hill

import boto3
import json

def ActivateLambdaNotifcation(deliverableMessage):
    lambdaClient = boto3.client('lambda')
    payload = {}
    payload["message"] = deliverableMessage
    response = lambdaClient.invoke(
        FunctionName='arn:aws:lambda:eu-west-1:924169754118:function:sendSNSfromChaosMonkey',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json.dumps(payload),
    )
    print("Sending notification to lambda")


