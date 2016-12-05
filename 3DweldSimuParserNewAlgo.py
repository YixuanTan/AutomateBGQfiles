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
remoteDirPrefix = '/gpfs/u/home/ACME/ACMEtany/scratch/MSMSEpaper/'
localDir = '/fasttmp/tany3/MSMSE2016/VolSizeMetric/PlayGround/NewAlgo/'
tmc_steps = [500,900, 1400,1900,2400,2800,3300,3800,4300,4800,5300,5900,5400,6900,7400]
time_points = [0.56219,0.99318, 1.5205,2.0395,2.5523,2.959, 3.4638,3.965, 4.4632,4.9588,5.452, 6.0411,6.5298,7.0168,7.5022]
r_fusion = [0.0083418,0.0085115,0.0086835,0.0088578,0.0090343,0.0092131,0.0093941,0.0095774,0.0097629,0.0099506,0.010141, 0.010333, 0.010527, 0.010724, 0.010923]
folders = ['3DweldNewAlgo']
# user defined parameter above
subfolders = ['1','2','3','4','5']

filePrefix = 'voronmc.'
fileSuffix = '.dat'
width = 5;

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)
sftp = ssh.open_sftp()

outputname = 'raw.dat'
transientname = 'rawc.dat'
localrecoder = 'result.txt'

cmd = 'module load gcc/4.9.2'
os.system(cmd)

for foldername in folders:
    for subfolder in subfolders:
        remoteDir = remoteDirPrefix + str(foldername) + '/' + subfolder + '/'
        sftp.chdir(remoteDir)
        outputname = 'raw.dat'
        transientname = 'rawc.dat'
        for i in range(len(tmc_steps)):
            label = tmc_steps[i]
            formatted = (width - len(str(label))) * "0" + str(label)
            file = filePrefix + formatted + fileSuffix
            sftp.get(file, localDir + outputname)
            # run wrongendian.out
            cmd = '/users/tany3/Downloads/wrongendian.out ' + localDir + outputname + ' ' + localDir + transientname
            os.system(cmd) 

            time = time_points[i]
            fusion = r_fusion[i]

            args = ['/users/tany3/Downloads/mmsp2vtkHaz', localDir + transientname, localDir + 'output.vtk', str(1878.0), str(time), str(fusion), '0.0005']
            popen = subprocess.Popen(args, stdout=subprocess.PIPE)
            popen.wait()
            output = popen.stdout.read()
            #print args
            f = open(localDir + localrecoder, "aw")
            f.write(output)
            f.close()

            args = ['/users/tany3/Downloads/mmsp2vtkHaz', localDir + transientname, localDir + 'output.vtk', str(1878.0), str(time), str(fusion), '0.002']
            popen = subprocess.Popen(args, stdout=subprocess.PIPE)
            popen.wait()
            output = popen.stdout.read()
            #print args
            f = open(localDir + localrecoder, "aw")
            f.write(output)
            f.close()

            args = ['/users/tany3/Downloads/mmsp2vtkHaz', localDir + transientname, localDir + 'output.vtk', str(1878.0), str(time), str(fusion), '0.007']
            popen = subprocess.Popen(args, stdout=subprocess.PIPE)
            popen.wait()
            output = popen.stdout.read()
            #print args
            f = open(localDir + localrecoder, "aw")
            f.write(output)
            f.close()

