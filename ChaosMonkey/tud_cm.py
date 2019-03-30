# -*- coding: utf-8 -*-
#
# Author: Dave Hill
# Chaos monkey code will list EC2s and knock X number out depending on input and trigger a notification

import boto3
import random
import time
from lambda_notification import ActivateLambdaNotifcation

# To test direct interaction with SNS notifications uncomment the below line and update the bottom line
# from notification import sendSNSNotification

TIME_TO_REVIVE = 600


##############################
# All my glorious utilities  #
##############################

# converts the annoying iterable format for EC2s to nice list for manipulation
def convertEC2iterToList(instances):
    myBeautifulList = []
    for instance in instances:
        myBeautifulList.append(instance.id)
    return myBeautifulList

# Gets the AWS account details to ensure we're using the right account
def accountDetails():
    stsclient = boto3.client('sts')                 # STS stands for Security Token Service
    myDetails = stsclient.get_caller_identity()
    print("Account ID = ", myDetails["Account"])
    print("User ID = ", myDetails["UserId"])

# gets the list of EC2 instances running as an iterable object
def getEc2instances():
    ec2client = boto3.resource('ec2')
    instances = ec2client.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])   # this filter ensures we only get running EC2s
    return instances

# counts the EC2 instances in the iterable object passed in.
def countEc2instances(instances):
    numInstances = 0
    for instance in instances:
        numInstances = numInstances+1
    return numInstances

# prints a list of the EC2 instances running in the account to the console
def printEc2instances(instances):
    for instance in instances:
        print(instance.id, instance.state["Name"])

# kills an EC2 instance based on ID
def killAnInstance(target):
    evilMonkeyClient = boto3.client('ec2')
    response = evilMonkeyClient.terminate_instances(
        InstanceIds=[target]
    )

# timing the reestablishment of VMs back to original numbers
def timingRebuild(total):
    machines = 0
    timeForFunction = time.time()       # Grab current time
    while machines < total:             # continue checking the machines until it matches the original number
        testing = getEc2instances()
        machines = countEc2instances(testing)
        if time.time() - timeForFunction > TIME_TO_REVIVE:  # Implement time limit for revival checks
            return "Failed"
    return "Passed"

# Picks X number of instances to kill
def breakingStuff(amount):
    currentInstances = getEc2instances()
    currentInstancesAsList = convertEC2iterToList(currentInstances)
    while int(amount) > 0:
        nextTarget = random.choice(currentInstancesAsList)
        currentInstancesAsList.remove(nextTarget)
        instancesImpactedStr = "The following instance ID {} will be disrupted:".format(nextTarget)
        print(instancesImpactedStr)
        killAnInstance(nextTarget)
        amount = amount - 1


##########################################
# The actual code that runs ChaosMonkey  #
##########################################


print("Welcome to the TUD Chaos Monkey!")
print("Checking AWS ...")

# Check which AWS account is in use
accountDetails()

# initial infrastructure assessment
runningMachines = getEc2instances()
printEc2instances(runningMachines)
instanceCount = countEc2instances(runningMachines)

instanceCountStr = "You current have {} instances running".format(instanceCount)
print(instanceCountStr)

# Get the number of instances to kill with some validation
monkeyShouldSmash = input("How many instances would you like to disrupt? ")

if int(monkeyShouldSmash) == 0:
    monkeyShouldSmash = input("This is going to be pretty dull if we don't disrupt SOME of these instances...Try again ")
    if int(monkeyShouldSmash) == 0:
        print("Well if you're not going to take this seriously...")
        raise SystemExit

while int(monkeyShouldSmash) > instanceCount:
    monkeyShouldSmash = input("...You just saw how many is there, you know you asked for two many, try again ")

print("Please wait while we unleash the chaos monkey...")

# chaos begins here
breakingStuff(int(monkeyShouldSmash))

# tracking time after killing instances to track revival time
startTime = time.time()

# confirm updated EC2 instances
updatedRunningMachines = getEc2instances()
printEc2instances(updatedRunningMachines)
updatedInstanceCount = countEc2instances(updatedRunningMachines)
updatedInstanceCountStr = "You now have {} instances running".format(updatedInstanceCount)
print(updatedInstanceCountStr)

# start checking repeatedly for the machines to have recovered
print("Now timing reinstatement")
print("Please wait while we test our recoverability")
result = timingRebuild(instanceCount)

# grab end time to calculate recovery time
endTime = time.time()
resultForNotification = ""

print("====CHAOS MONKEY TEST RESULT====")

# time to recover obtained
testTime = endTime - startTime

# build test results output
if result == "Passed":
    testResultStr = "It took {} seconds to get back to {} instances".format(testTime, instanceCount)
    print(testResultStr)
    resultForNotification = "Dave Hill's TUD_CM test PASSED. "+testResultStr
elif result == "Failed":
    testResultStr = "Chaos Monkey has won. We have not gotten back to the original number of instances. Goodbye"
    print(testResultStr)
    resultForNotification = "Dave Hill's TUD_CM test FAILED. " + testResultStr
else:
    print("Something has gone wrong in the test, Dave should debug further")
    resultForNotification = "While the test goofed, you got a notification still from Dave Hill, yay!"

# Activate the reporting lambda
ActivateLambdaNotifcation(resultForNotification)
