# -*- coding: utf-8 -*-

import sys
import boto3

print ("Welcome to the TUD Chaos Monkey!")

num = 4

instanceCountStr = "You current have {} instances running".format(num)

print (instanceCountStr)

monkeyShouldSmash = input("How many instances would you like to disrupt?")

instancesImpactedStr = "The following {} instance ID(s) will be disrupted:".format(monkeyShouldSmash)

print(instancesImpactedStr)
print("Please wait while we unleash the chaos monkey...")

updatedNum = 2

updatedInstanceCountStr = "You now have {} instances running".format(updatedNum)

print (updatedInstanceCountStr)


print ("Now timing reinstatement")
print {"Please wait while we test our recoverability"}

print (instanceCountStr)

print ("====CHAOS MONKEY TEST RESULT====")

