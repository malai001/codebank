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

host_n = 'vm-sipproxy2'
stdout_data = []
stderr_data = []
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect( hostname = hostname , username = username, password =password)
#session = client.open_channel(kind='session')
#session.exec_command(command)

cmd = 'cd /home/kesavCARepository/;./create_cert.sh -CN '+host_n+' -host '+host_n+';cd repository/;ls -t;'
cmd1 = 'cd /home/kesavCARepository/;cd repository/;ls -t;'
stdin, stdout, stderr = ssh.exec_command(cmd1)
stdout_data = stdout.readlines()
Files = stdout_data[:4]
print Files
s = []
a = Files[0]
Files[0] =a[:-1]
a = Files[1]
Files[1] =a[:-1]
a = Files[2]
Files[2] =a[:-1]
a = Files[3]
Files[3] =a[:-1]

os.system('pscp -pw root123 root@172.24.133.76:/home/kesavCARepository/repository/'+stdout_data[1]+' C:\\TLS_Certificates\\')
os.system('pscp -pw root123 root@172.24.133.76:/home/kesavCARepository/repository/'+stdout_data[2]+' C:\\TLS_Certificates\\')
os.system('pscp -r -pw root123 root@172.24.133.76:/home/kesavCARepository/ca_conf C:\\TLS_Certificates\\')
os.system('certutil -delstore -enterprise "Root" 172.24.133.76-CA')
os.system('certutil -delstore -user "Root" 172.24.133.76-CA')
os.system('certutil -delstore -user "MY" "vm-sipproxy2"')
os.system('certutil -delstore "MY" "vm-sipproxy2"')
os.system('certutil -addstore -f -enterprise "Root" C:\TLS_Certificates\ca_conf\ca_cert.pem')#LocalMcahine_Trustedroot
os.system('certutil -addstore -f -user "Root" C:\TLS_Certificates\ca_conf\ca_cert.pem')#
for i in Files:
	print i
	if i .endswith('.pfx'):
		File_cmd_usr = 'certutil -f -p "" -user -importpfx C:\TLS_Certificates\\'+i 
		File_cmd_rt  = 'certutil -f -p "" -importpfx C:\TLS_Certificates\\'+i 
os.system(File_cmd_usr)
os.system(File_cmd_rt)
print "Successfully downloaded and installed"
ssh.close()
# certutil -delstore -enterprise "Root" 172.24.133.76-CA
# certutil -addstore -f -enterprise "Root" C:\Users\ca_conf\ca_cert.pem
# certutil -f -p "" -user -importpfx C:\TLS_Certificates\\
# certutil -delstore -user "MY" "vm-sipproxy2"
# certutil -delstore "MY" "vm-sipproxy2"
# certutil -addstore -f -p "" -user -importpfx c:\TLS_Certificates\\+i
