# -*- coding: utf-8 -*-
#
# Author: Dave Hill

import sys
import boto3
import random
import time
from notification import sendSNSNotification

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
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
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
    timeForFunction = time.time()
    while machines < total:
        testing = getEc2instances()
        machines = countEc2instances(testing)
        if time.time() - timeForFunction > 600:
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

accountDetails()

runningMachines = getEc2instances()
printEc2instances(runningMachines)
instanceCount = countEc2instances(runningMachines)

instanceCountStr = "You current have {} instances running".format(instanceCount)
print(instanceCountStr)

monkeyShouldSmash = input("How many instances would you like to disrupt? ")

if int(monkeyShouldSmash) == 0:
    monkeyShouldSmash = input("This is going to be pretty dull if we don't disrupt SOME of these instances...Try again ")
    if int(monkeyShouldSmash) == 0:
        print("Well if you're not going to take this seriously...")
        raise SystemExit

while int(monkeyShouldSmash) > instanceCount:
    monkeyShouldSmash = input("...You just saw how many is there, you know you asked for two many, try again ")


print("Please wait while we unleash the chaos monkey...")


breakingStuff(int(monkeyShouldSmash))

startTime = time.time()


updatedRunningMachines = getEc2instances()
printEc2instances(updatedRunningMachines)
updatedInstanceCount = countEc2instances(updatedRunningMachines)

updatedInstanceCountStr = "You now have {} instances running".format(updatedInstanceCount)

print(updatedInstanceCountStr)


print("Now timing reinstatement")
print("Please wait while we test our recoverability")
result = timingRebuild(instanceCount)
endTime = time.time()
resultForNotification = ""

#print(instanceCountStr)

print("====CHAOS MONKEY TEST RESULT====")

testTime = endTime - startTime

if result == "Passed":
    testResultStr = "It took {} seconds to get back to {} instances".format(testTime, instanceCount)
    print(testResultStr)
    resultForNotification = "Dave Hill's TUD_CM test PASSED. "+testResultStr
    #raise SystemExit
elif result == "Failed":
    testResultStr = "Chaos Monkey has won. We have not gotten back to the original number of instances. Goodbye"
    print(testResultStr)
    resultForNotification = "Dave Hill's TUD_CM test FAILED. " + testResultStr
else:
    print("Something has gone wrong in the test, Dave should debug further")
    resultForNotification = "While the test goofed, you got a notification still from Dave Hill, yay!"

sendSNSNotification(resultForNotification)
