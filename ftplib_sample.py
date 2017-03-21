import ftplib

# new1="notroot"
# new2= "genesys"
# datanew = "135.225.59.70"

new1="administrator"
new2= "(Genesys)"
datanew = "172.24.130.182"
appConfigPath1 = 'C:\Program Files (x86)\GCTI\SIP Endpoint SDK\TestSampleExe\SipEndpoint.config'
c = ftplib.FTP(datanew,new1,new2)
print "opened an ftp connection"
macConfigPath = '/Program Files (x86)/GCTI/SIP Endpoint SDK'

c.cwd(macConfigPath)   
print 'set Success'             
ff = open(appConfigPath1, 'rb')
c.storbinary('STOR SipEndpoint.config', ff)
print "stored the file"
c.quit()

ff.close()