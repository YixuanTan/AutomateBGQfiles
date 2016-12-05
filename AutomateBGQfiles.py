import os
import paramiko
import sys
import subprocess

if len(sys.argv) != 2:
    print "args missing"
    sys.exit(1)


# user defined parameter below:
hostname = 'lp02.cci.rpi.edu'
password = sys.argv[1];
username = 'ACMEtany'
port = 22
outputnamePrefix = '2dfit_'
remoteDirPrefix = '/gpfs/u/home/ACME/ACMEtany/scratch/MSMSEpaper/2Dfit/'
localDir = '/fasttmp/tany3/MSMSE2016/VolSizeMetric/2DfitMc/'
startFolderNumber = 6;
endFolderNumber = 15;
totalTmc = 50000
increment = 100
# user defined parameter above


filePrefix = 'voronmc.'
fileSuffix = '.dat'

width = len(str(totalTmc));

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)
sftp = ssh.open_sftp()

cmd = 'module load gcc/4.9.2'
os.system(cmd)

for folderNumber in range(startFolderNumber, endFolderNumber + 1, 1):
    remoteDir = remoteDirPrefix + str(folderNumber) +'/'
    sftp.chdir(remoteDir)
    outputname = outputnamePrefix + str(folderNumber) + '.txt'
    for label in range(increment, totalTmc, increment):
        formatted = (width - len(str(label))) * "0" + str(label)
        file = filePrefix + formatted + fileSuffix
        sftp.get(file, localDir + file)
        
        #  USER DEFINED CODE BLOCK
        cmd = '/users/tany3/Downloads/wrongendian.out ' + localDir + file + ' ' + localDir + file + 'c'
        os.system(cmd) 

        args = ['/users/tany3/Downloads/CountGrain', localDir + file + 'c']
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()
        #print output
        f = open(localDir + outputname, "aw")
        f.write(output)
        f.close()

        # clean 
        cmd = 'rm ' + localDir + filePrefix + '*'
        os.system(cmd)



