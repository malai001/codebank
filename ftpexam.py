from ftplib import FTP
ftp = FTP('mac1','notroot','Admin123')
#ftp.login()
ftp.cwd('/Users/notroot/Desktop/SDK/Bin/')
ftp.retrlines('LIST')
