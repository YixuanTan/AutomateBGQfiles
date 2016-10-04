import os
import paramiko
import sys

if len(sys.argv) != 2:
    print "args missing"
    sys.exit(1)

hostname = 'lp02.cci.rpi.edu'
password = sys.argv[1];
username = 'ACMEtany'
port = 22

remoteDir = '/gpfs/u/home/ACME/ACMEtany/scratch/MSMSEpaper/2DfitMc/1/'
localDir = '/fasttmp/tany3/MSMSE2016/VolSizeMetric/test/'
filePrefix = 'voronmc.'
fileSuffix = '.dat'

totalTmc = 50000
increment = 5000

width = len(str(totalTmc));

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)
sftp = ssh.open_sftp()

sftp.chdir(remoteDir)

for label in range(increment, totalTmc, increment):
    formatted = (width - len(str(label))) * "0" + str(label)
    file = filePrefix + formatted + fileSuffix
    sftp.get(file, localDir + file)

