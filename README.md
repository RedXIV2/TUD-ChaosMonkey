# TUD-ChaosMonkey
Chaos Monkey simulation to test High Availability in AWS

This application is built using Python 3 and utilising the Boto3 library to connect to AWS. By utilising the AWS credentials locally, this utility will grab a list of any EC2 instances associated with the account that are running. The user can then choose a subset of these instances randomly to test the recoverability of these machines. 

There is a configurable limit, currently set to **10** minutes, which marks the point where the recoverability is evaluated as a failed. 

For a detailed walkthough of the project please visit the following URL for an explanation of the code:
[Walkthorugh hosted on YouTube](https://www.youtube.com/watch?v=_le6GJitDxU&feature=youtu.be "Link To YouTube")


----
## Prerequisites

- Python 3
- boto3
- AWS credentials configured

-----

## Usage
1. Open command prompt/terminal
2. Navigate to the directory with the "tud_cm.py" file 
3. Initiate the program by calling "python tud_cm.py" 
4. Follow Instructions offered by program during execution

---

## Troubleshooting

If you having issues getting this to work, please feel free to contact me. Especially if it's the difference in a grade.

