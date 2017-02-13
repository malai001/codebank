class SipEp_Net():
	'''This class contain the basic function for sipendpoint automation'''
    def Endpoint_StatusCheck(self,id=0):
        if id:
            appPath1 = tempPath
        else:
            appPath1 = appPath
        cwd = os.getcwd()
        os.chdir(appPath1)
        if os.system('start ' + appName):
            time.sleep(5)
            os.chdir(cwd)
            print "%s Started successfully" % appName
            return 1
        else:
            return 0
