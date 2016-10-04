import os
import paramiko
import sys
import subprocess
import time

if len(sys.argv) != 2:
    print "args missing"
    sys.exit(1)

hostname = 'lp01.cci.rpi.edu'
password = sys.argv[1];
username = 'ACMEtany'
port = 22

outputname = 'out.txt'
remoteDir = '/gpfs/u/home/ACME/ACMEtany/scratch/MSMSEpaper/2DfitMc/1/'
localDir = '/fasttmp/tany3/MSMSE2016/VolSizeMetric/2DfitMc/'
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
    
    #  USER DEFINED CODE BLOCK
    #time.sleep(5)
    #command = ['/users/tany3/Downloads/wrongendian.out ', localDir + file, localDir + file + 'c']
    #print 'command1 ', command
    #call(command)
    cmd = '/users/tany3/Downloads/wrongendian.out ' + localDir + file + ' ' + localDir + file + 'c'
    os.system(cmd) 
    #time.sleep(10)

    #f = open(localDir + outputname, "aw")
    #command = '/users/tany3/Downloads/mmsp2xyz ' + localDir + file + 'c' + ' ' + localDir + filePrefix + formatted + '.txt'
    #print 'command2 ', command
    #call(command, stdout=f)
    args = ('/users/tany3/Downloads/mmsp2xyz', localDir + file + 'c', localDir + filePrefix + formatted + '.txt')
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print output
    f = open(localDir + outputname, "aw")
    f.write(output + '\n\n')

    # clean 
    cmd = 'rm ' + localDir + filePrefix + '*'
    os.system(cmd)
    #os.remove(localDir + filePrefix + '*')


