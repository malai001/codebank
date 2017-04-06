import paramiko
import sys
import os

nbytes = 4096
hostname = '172.24.133.76'
port = 22
username = 'root' 
password = 'root123'
command = 'cd /'

#client = paramiko.Transport((hostname, port))
#client.connect(username=username, password=password)

stdout_data = []
stderr_data = []
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect( hostname = hostname , username = username, password =password)
#session = client.open_channel(kind='session')
#session.exec_command(command)

stdin, stdout, stderr = ssh.exec_command('cd /home/kesavCARepository/repository;ls -t;')
stdout_data = stdout.readlines()
print stdout_data[:4]
s = []

sftp = ssh.open_sftp()
local_path = 'C:\\Users\\aarumuga\\Desktop\\New folder\\'
local_path = os.path.join(local_path,'abc.pem')
remote_path = '/home/kesavCARepository/repository/'
remote_path += stdout_data[0]
#local_path  += 'a.pem'
print local_path
print remote_path
sftp.put(local_path,remote_path)
#sftp.get(remote_path,local_path)
sftp.close()
# cmd2 = 'cat /home/dir/test.log'
# self.ssh_stdin2, self.ssh_stdout2, self.ssh_stderr2 = self.ssh.exec_command(cmd2)
# print self.ssh_stdout2.read()


# while True:
#     if session.recv_ready():
#         stdout_data.append(session.recv(nbytes))
#     if session.recv_stderr_ready():
#         stderr_data.append(session.recv_stderr(nbytes))
#     if session.exit_status_ready():
#         break

# print 'exit status: ', session.recv_exit_status()
#print ''.join(stdout_data)
#print ''.join(stderr_data)

ssh.close()
