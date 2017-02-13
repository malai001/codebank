#from model_base_client import Client
from common import *
from common_enum import CallState, EventName, CfgAppType
import default_servers  
import time
import re
from common import SeriousError as CommonSeriousError
from common import Error as CommonError
from common import Warning as CommonWarning
from model import ServerContainer
import telnetlib

epiConnections = {}

class EpiClient(telnetlib.Telnet):
  def __init__(self, host, port):
    self.Connection = 0
    self.host = host
    self.port = port
    try:
      telnetlib.Telnet.__init__(self, host, port)
      self.connectionMessage = self.Wait()
    except Exception, mess:
      CommonSeriousError(1, "Connection to %s %s cannot be established: %s" %(host, port, str(mess)))
    self.Connection = 1
  
  def Send(self, data, printTo = 1):
    if printTo:
      PrintLog( "Command sent: " + data)
    try:
      self.write(data)
    except Exception, mess:
      CommonSeriousError(1, mess)

  
  def Wait(self, timeout = 3, printTo = 1):
    try:
      data = self.read_until("\r\n", timeout)
    except Exception, mess:
      CommonSeriousError(1, mess)
    if printTo:
      PrintLog("Received message: " + data)
    return data
  
  def Close(self):
    if self.Connection:
      PrintLog("Closing connection to %s %s" %(self.host, self.port))
      self.close()
    if epiConnections.has_key(self.host + str(self.port)): del epiConnections[self.host + str(self.port)]
      
    


def GetEpiConnection(host, port):
  if epiConnections.has_key(host + str(port)):
    epiConnection = epiConnections[host + str(port)]
  else:
    epiConnection = EpiClient(host, int(port))
    epiConnection.bufferLength = 16384
    if not epiConnection.Connection:
      epiConnection = None
    epiConnections[host + str(port)] = epiConnection
  return epiConnection


class SipPhoneEpiCommon:
  def __init__(self, phone, host = None, port = 0):
    #connect to epiphone
    self.phone = phone
    self.globalName = "Epiphone"
    self.defaultMethodDTMF = 'rfc2833'
    self.epiHost = host
    self.epiPort = port
    if not self.phoneClient():
      FatalError("No connection to EpiPhone")
    ind1 = self.phoneClient().connectionMessage.find("<")
    ind2 = self.phoneClient().connectionMessage.find(">")
    self.contact = ""
    if ind1 <> -1 and ind2 <> -1:
      self.contact = self.phoneClient().connectionMessage[ind1+1:ind2][4:]
    self.requestTimout = 0
    self.printTo = 0
    if InTrue(GetOption("DebugLevel")): self.printTo = 1
    if InFalse(GetOption("SIP:NoCleanupPhoneAtStart")):
      self.Cleanup()                                   # cleanup the phone before testing    

  def Reconnect(self):
    if epiConnections.has_key(self.epiHost + str(self.epiPort)):
      del epiConnections[self.epiHost + str(self.epiPort)]
    GetEpiConnection(self.epiHost, self.epiPort)
    
  def phoneClient(self):
    return GetEpiConnection(self.epiHost, self.epiPort)
    
  def Clear(self):
    pass
  
  def UsualCleanUp(self):
    pass
    

  def Cleanup(self):
    """drops all active SIP dialogs (sending BYE but not waiting for response) and revert all 
    temporary configuration changes back to file value (that includes "on-invite/mkcall-once" 
    custom SIP scripts, the rest of CSS is discarded along with dialogs
    """
    request = 'cleanup\r\n'
    PrintLog("\nSend request to EpiPhone %s" %request)
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    if response:
      PrintLog('Cleanup: %s' %response)
      
  def SipRegisterAll(self):
    PrintLog('\nSend request to EpiPhone: SIP REGISTER FOR ALL SIP ENDPOINTS')
    request = 'connect\r\n'
    self.phoneClient().Send(request, printTo = self.printTo)
    self.phoneClient().Wait(printTo = self.printTo)

    
  def Play(self, scenario, caps = 0, count = 0, repeat = 0):
    
    request = 'play,case="%s"'%scenario
    if repeat:
      request = request + ",repeat=%d\r\n"%repeat
    elif (caps and count):
      request = request + ",caps=%s,count=%s\r\n"%(caps,count)
    else:
      request = request + "\r\n"
    PrintLog('\nSend request to EpiPhone: %s '%request)
    self.phoneClient().Send(request, printTo = self.printTo)
    self.phoneClient().Wait(printTo = self.printTo)
   
  def Stop(self, scenario):
    
    request = 'stop,case="%s"\r\n'%scenario
    PrintLog('\nSend request to EpiPhone: %s '%request)
    self.phoneClient().Send(request, printTo = self.printTo)
    self.phoneClient().Wait(printTo = self.printTo)    
    
  def Close(self):
    self.Clear()

  
  
  def Warning(self, str1 = "", str2 = ""):
    if self.tDN:
      if self.tDN.tserver.appGCTIType == "VirtualTserver":
        CommonWarning(str1, str2)
      else:
        self.tDN.master.Warning(str1, str2)
        self.tDN.master.warBadOtherCnt = self.tDN.master.warBadOtherCnt + 1
    else:
      CommonWarning(str1, str2)  
    
  def Error(self, str1 = "", str2 = ""):
    if self.tDN:
      if self.tDN.tserver.appGCTIType == "VirtualTserver":
        CommonError(str1, str2)
      else:
        self.tDN.master.Error(str1, str2)
        self.tDN.master.errBadOtherCnt = self.tDN.master.errBadOtherCnt + 1
    else:
      CommonError(str1, str2)  
  
  
  def SeriousError(self, str1 = "", str2 = "", forceReset = -1):
    if forceReset == 1:
      tservers = []
      for server in ServerContainer():
        if server.cfgApp and server.cfgApp.type == CfgAppType.CFGTServer.val:
          tservers.append(server)
      for tserver in tservers:
        tserver.SetTestResult(TestResEnum.ForceReset)
        
    if self.tDN:
      if self.tDN.tserver.appGCTIType == "VirtualTserver":
        if forceReset == -1: forceReset = GetOption("ResetTestAfterError")

        CommonSeriousError(forceReset, str1, str2)
      else:
        self.tDN.master.serErrBadOtherCnt = self.tDN.master.serErrBadOtherCnt + 1
        self.tDN.master.SeriousError(str1, str2, forceReset)
        
    else:
      if forceReset == -1: forceReset = GetOption("ResetTestAfterError")
      #PrintLog("Calling CommonSeriousError (str1 = %s, str2 = %s)" %(str1, str2))
      CommonSeriousError(forceReset, str1, str2)
    
  def parseResponse(self, request, response):
    
    dnName = "%s %s" %(self.globalName, self.phone)
    if response:
      pat = "\((.*)\)"
      mo = re.match(pat, response, re.DOTALL)
      if mo:
        cmd = mo.group(1)
        res = cmd.split(",")
        if len(res) == 2:
          code = res[0].strip()
          if code <> "200":
            
            self.SeriousError("Bad result on %s on request %s to EpiPhone: %s" %(dnName, request, response), forceReset = 1)
          pat = "id\s*=\s*(.+)"
          mo = re.match(pat, res[1].strip(), re.DOTALL)
          if not mo:
            self.SeriousError("Bad result on %s on request %s to EpiPhone: %s (cannot parse)" %(dnName, request, response), forceReset = 1)
          id = mo.group(1)
          PrintLog("  Result on request: %s code = %s, id = %s" %(dnName, code, id))
        else:
             
          self.SeriousError("Bad result on %s on request %s to EpiPhone: %s (cannot parse 1)" %(dnName, request, response), forceReset = 1)
      else:
           
        self.SeriousError("Bad result on %s on request %s to EpiPhone: %s (cannot parse 2)" %(dnName, request, response), forceReset = 1)
    else:
         
      self.SeriousError("Bad result on %s on request %s to EpiPhone (no response)" %(dnName, request), forceReset = 1)
    return code, id
    
  def parseResponseQuery(self, request, response):
    dnName = "%s %s" %(self.globalName, self.phone)
    if response:
      pat = "\((.*)\)"
      mo = re.match(pat, response, re.DOTALL)
      if mo:
        cmd = mo.group(1)
        res = cmd.split(",")
      
        if len(res) >= 2:
          code = res[0].strip()
          id = ""
          Rx = []
          ps = ""
          ac = ""
          st = ""
          peer = ""
          result = {}
          for otherInfo in res:
            pat = "Rx\s*=\s*\((.+)\)"
            mo = re.match(pat, otherInfo.strip(), re.DOTALL)
            if mo:
              Rx = mo.group(1)
              Rx = Rx.split(";")
            else:
              pat = "ps\s*=\s*\"(.+)\""
              mo = re.match(pat, otherInfo.strip(), re.DOTALL)
              if mo:
                ps = mo.group(1)
              else:
                pat = "id\s*=\s*(.+)"
                mo = re.match(pat, otherInfo.strip(), re.DOTALL)
                if mo:
                  id = mo.group(1)
                else:
                  pat = "ac\s*=\s*\"(.+)\""
                  mo = re.match(pat, otherInfo.strip(), re.DOTALL)
                  if mo:
                    ac = mo.group(1)
                  else:
                    pat = "st\s*=\s*\"(.+)\""
                    mo = re.match(pat, otherInfo.strip(), re.DOTALL)
                    if mo:
                      st = mo.group(1)
                    else:
                      pat = "peer\s*=\s*(.+)"
                      mo = re.match(pat, otherInfo.strip(), re.DOTALL)
                      if mo:
                        peer = mo.group(1)                       
          result = {"code": code, "id": id, "Rx": Rx, "ps": ps, "ac": ac, "st": st, "peer": peer}
#          PrintLog("parseResponseQuery:\n\tQuery result on %s  %s" %( dnName, result))
          return result 
  

        else:
             
          self.SeriousError("Bad result on %s on request %s to EpiPhone: %s (cannot parse 1)" %(dnName, request, response), forceReset = 1)
      else:
           
        self.SeriousError("Bad result on %s on request %s to EpiPhone: %s (cannot parse 2)" %(dnName, request, response), forceReset = 1)
    else:
         
      self.SeriousError("Bad result on %s on request %s to EpiPhone (no response)" %(dnName, request), forceReset = 1)
    
  def parseGetSIPResponse(self, request, response):
    """returns code, id, message. if request is for specific message, message
       is returned as dictionary; otherwise (sip history) message returned as string
    """
    if response:
      code = 0
      id = 0
      msg = ""
      pat = "\((.*)\)"
      mo = re.match(pat, response, re.DOTALL)
      if mo:
        cmd = mo.group(1)
        pat = "(\d+),id=(\d+),([sipmsg]{3}=\((.+)\))"
        mo = re.match(pat, cmd, re.DOTALL)
        if mo:
          code = mo.group(1)
          id = mo.group(2)
          msg = mo.group(4)
        else:
          pat = "(\d+),([sipmsg]{3}=\((.+)\))"
          mo = re.match(pat, cmd, re.DOTALL)
          if mo:
            code = mo.group(1)
            msg = mo.group(3)
          else:
            pat = "(\d+),(.+)"
            mo = re.match(pat, cmd, re.DOTALL)
            if not mo:
              self.SeriousError("Bad result on request %s to EpiPhone: %s (cannot parse 2)" %( request, response), forceReset = 1)
            else:
              code = mo.group(1)
              msg = mo.group(2)  
#        PrintLog('\tResult on request: code = %s, id = %s, msg = "%s"' %( code, id, msg))              
      else:
           
        self.SeriousError("Bad result on request %s to EpiPhone: %s (cannot parse 2)" %( request, response), forceReset = 1)
    else:
         
      self.SeriousError("Bad result on request %s to EpiPhone (no response)" %( request), forceReset = 1)
    if request.find("msg=") <> -1:
      msg = self.parseSipMessage(msg)
    # To make behavior consistent. id should be Integer
    if id:
      try:
        id=int(id)
      except:
        self.SeriousError("Bad result on request %s to EpiPhone: %s (returned non-numeric sipCallID - epiID)" % (request, response))
    return code, id, msg

 
  def parseSipMessage(self, msg):
    pat = r'([^"]+)="(.*?(?<!\\))"(,?)'
    o = re.compile(pat, re.DOTALL)
    ms = o.findall(msg)
    result = {}
    for pair in ms:
      key, value, comma = pair
      if value.find("\x5c\x22") <> -1:
        value = value.replace("\x5c\x22", "\x22") 
      if result.has_key(key):
        if type(result[key]) == type(""):
          result[key] = [result[key]] + [value]
        else:
          result[key].append(value)
      else:
        result[key] = value
    return result
  



  def SetConfig(self, confStr = None, pipe = 0):
    """Send request config to EpiPhone, waits for response
       Raises 'Serious Error' when EpiPhone returns negative responce
       parameters
          confStr - str, e.g  sip='ring', sip='DN4'
          pipe - for dn SetConfig 'pipe=0'/for pipe SetConfig 'pipe=1'
       return
          result
    """
    idStr = ""
    if confStr:
      idStr = ",%s"%confStr    
    if pipe:
      request = 'config,pipe="%s"%s\r\n' %(self.phone, idStr)
    else:
      request = 'config,dn="%s"%s\r\n' %(self.phone, idStr)
    PrintLog("\n---Send request to EpiPhone %s" %request.rstrip())
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    if not response:
      self.SeriousError("Bad result on %s on request %s to EpiPhone (no response)" %(self.phone, request), forceReset = 1)    
    PrintLog("   %s" %response.rstrip())
    if not re.match('\(200,st=.*',response):
      self.SeriousError('Bad result on request "%s" to EpiPhone: %s'%(request.rstrip(), response.rstrip()), forceReset = 1)
    return response
  
  def QueryAll(self, realPartiesOnly=False):
    """Send request query to EpiPhone, waits for response
       parameters
         realPartiesOnly - boolean parameter. Default value = False.
                            If set to True - doesn't include EpiPhone response '481', 'call not found' into function
                            result. It means that response length will be 0 in this case.
       return
          response - list of dictionaries:
            [
            {'ps': 'alerting', 'ac': 'pcmu', 'code': '120', 'Rx': [], 'st': '', 'id': '39'},
            {'ps': 'alerting', 'ac': '', 'code': '200', 'Rx': [], 'st': '', 'id': '40'}
            ...,
            ]
    """
    request = 'query,dn="%s",ps=all\r\n' %self.phone
    PrintLog('\n---Send request to EpiPhone: query,dn="%s",ps=all'%self.phone)
    self.phoneClient().Send(request, printTo = self.printTo)
    
    firstTime = 1
    QueryAllResp = []
    while 1:
      if firstTime:
        waitTimeout = 3
      else:
        waitTimeout = 0.1
      resp = self.phoneClient().Wait(printTo = self.printTo, timeout = waitTimeout)
      firstTime = 0
      if not resp: break
      QueryAllResp.append(resp)
    if not QueryAllResp:    
      self.SeriousError("Bad result on %s on request %s to EpiPhone (no response)" %(dnName, request), forceReset = 1)    
    results = []
    for dialog in QueryAllResp:
      if dialog:
        PrintLog('    %s'%dialog)
        result = self.parseResponseQuery(request, dialog)
        if realPartiesOnly and result.get("code", "481") == "481":
            continue
        results.append(result)
    return results
  
  def Query(self, sipCallID = None, ps = None):
    """Send request query to EpiPhone, waits for response
       parameters: 
         CallID,
         ps (a.k.a -PartyState (values:initiated, alerting, connected, held))
       return
          response - message parsed to dict: {'ps': 'PartyState', 'ac': "codec", 'code': 'xx0', 'Rx': [tones, detected], 'id': 'CallID', 'peer': 'peer'}
    """
    idStr = ""
    psStr = ""
    if sipCallID:
      idStr = ",id=%s"%sipCallID
    psStr = ""
    if ps:
      psStr = ",ps=%s"%ps
    request = 'query,dn="%s"%s%s\r\n' %(self.phone, idStr, psStr)

    PrintLog('\n---Send request to EpiPhone: query,dn="%s"%s%s'  %(self.phone, idStr, psStr))
    self.phoneClient().Send(request, printTo = self.printTo)

    response = self.phoneClient().Wait(printTo = self.printTo)
    result = self.parseResponseQuery(request, response)
    return result
  


  def VerifySIPHistory(self, pattern, sipCallID = None, ps = None, dlg = None, error = 1):
    """Calls GetSIP for sip history
       Raises 'Serious Error' if pattern does not match
       the end of string returned by GetSIP
       parameters
         sipCallID - int
         pattern   - string, expected end of sip history 
         ps (a.k.a -PartyState (values:initiated, alerting, connected, held))
         dlg = None|inc|out: most recent incoming/outgoing SIP dialog ID OR 'dev' for query out of call content dialogs
     """
    PrintLog("\n---VerifySIPHistory at dn = %s, EpiID = %s, pattern = '%s', ps = %s, dlg = %s:" %(self.phone, sipCallID, pattern, ps, dlg))
    code, id, msg = self.GetSIP(sipCallID, None, ps, dlg)
    if not re.search(pattern + "$", msg):
      if not error:
        Warning("Received SIP history does not match pattern:\n\t\tPattern: %s\n\t\tHistory: %s" %(msg, pattern))
      else:
        self.SeriousError("Received SIP history does not match pattern:\n\t\tPattern: %s\n\t\tHistory: %s" %(pattern, msg))
    else:
      PrintLog("\tVerifySIPHistory at dn = %s, EpiID = %s, pattern matches\n---" %(self.phone, sipCallID))


  def VerifySIPMsg(self, msg, header = None, pattern = None, sipCallID = None, ps = None, dlg = None, skip = None, error = 1, exactMatch = "re", checkOrder = True):
    """Calls GetSIP for for specific message
       Raises 'Serious Error' if header is absent or pattern does not match msg[header] OR raise 'SeriousError' if header is present and pattern omitted.
       parameters
         msg       - specific message, valid  (for EpiPhone's GETSIP) values N|last|name
         header    - string
         pattern   - string or list, expected value of msg[header] or omitted (pattern=None)
         sipCallID - int
         ps (a.k.a -PartyState (values:initiated, alerting, connected, held))
         dlg = None|inc|out: most recent incoming/outgoing SIP dialog ID OR 'dev' for query out of call content dialogs
         skip - N parameter to getSIP,X,msg="name" query (to skip N messages from   back of the list matching given name in sip history)
         exactMatch - string or boolean, valid values "re", "re.I", True, False. Defines the way matching is performed. 
    """
    PrintLog("\n---VerifySIPMsg at dn = %s, msg = '%s', header = '%s', pattern = '%s', sipCallID = '%s', ps = '%s', dlg = '%s', skip = '%s', exactMatch = '%s', checkOrder = '%s'':" %(self.phone, msg, header, pattern, sipCallID, ps, dlg, skip, exactMatch, checkOrder))
    msg_incoming = msg
    event = None
    if isinstance(msg, str) and msg.startswith("<<NOTIFY"):
      try:
        event = msg.split("\"")[1]
      except IndexError:
        event = None
    code, id, msg = self.GetSIP(sipCallID, msg, ps, dlg, skip)
    if event:
      i = 1
      while "Event" in msg and msg["Event"] != event:
        code, id, msg = self.GetSIP(sipCallID, msg_incoming, ps, dlg, skip+i)
        i += 1

    if not pattern and msg.has_key(header):
      if not error:
        self.Warning("SIP message '%' contains unexpected header '%s'" %(msg, header)) 
      else: 
        self.SeriousError('SIP message contains unexpected header "%s"'%header)
      return 0
    elif not msg.has_key(header) and pattern:
      if not error:
        self.Warning("SIP message does not contain required header '%s'" %header) 
      else:      
        self.SeriousError("SIP message does not contain required header '%s'" %header)
      return 0
    elif not pattern and not msg.has_key(header):
      PrintLog("\tVerifySIPMsg at dn = %s, EpiID = %s: SIP message does not contain unexpected header '%s', exact match = %s, checkOrder = %s\n" %(self.phone, sipCallID, header, exactMatch, checkOrder))
      return 1
    else:
      if pattern:
        bad  = 0
        if type(pattern) == type([]): # expected duplicate headers
          if type(msg[header]) != type([]):
            bad = 1
          else: 
            
            if InTrue(checkOrder):
              if len(msg[header]) != len(pattern):
                bad = 1
              else:
                ind = 0
                for subPattern in pattern:
                  val  = msg[header][ind]
                  if exactMatch == "re":
                    if not re.search(subPattern, val):
                      bad = 1
                      break
                  elif exactMatch == "re.I":
                    if not re.search(subPattern, val,re.I):
                      bad = 1
                      break
                  elif exactMatch == "re.S":
                    if not re.search(subPattern, val, re.S):
                      bad = 1
                      break                    
                  elif InTrue(exactMatch):
                    if val != subPattern:
                      bad = 1
                      break
                  elif InFalse(exactMatch):
                    if  val.find(subPattern) == -1:
                      bad = 1
                      break
                  else:
                    ProgrammError("Incorrect value of parameter exactMatch. Valid values 're', 're.I','re.S', True, False")
                  ind = ind + 1
            else: #checkOrder == False
              found = 0
              for subPattern in pattern:
                for val in msg[header]:
                  if exactMatch == "re":
                    if re.search(subPattern, val):
                      found = 1
                      break
                  elif exactMatch == "re.I":
                    if re.search(subPattern, val,re.I):
                      found = 1
                      break
                  elif exactMatch == "re.S":
                    if re.search(subPattern, val, re.S):
                      found = 1
                      break                    
                  elif InTrue(exactMatch):
                    if val == subPattern:
                      found = 1
                      break
                  elif InFalse(exactMatch):
                    if val.find(subPattern) <> -1:
                      found = 1
                      break
                  else:
                    ProgrammError("Incorrect value of parameter exactMatch. Valid values 're', 're.I','re.S', True, False")
                    
                if not found: 
                  bad = 1
                  break #for subPattern in pattern cycle
        else:
          if type(msg[header]) == type([]):
            bad = 1
          else:
            if exactMatch == "re":
              if not re.search(pattern, msg[header]):
                bad = 1
            elif exactMatch == "re.I":
              if not re.search(pattern, msg[header],re.I):
                bad = 1
            elif exactMatch == "re.S":
              if not re.search(pattern, msg[header],re.S):
                bad = 1                
            elif InTrue(exactMatch):
              if msg[header] != pattern:
                bad = 1
            elif InFalse(exactMatch):
              if msg[header].find(pattern) == -1:
                bad = 1
            else:
              ProgrammError("Incorrect value of parameter exactMatch. Valid values 're', 're.I', 're.S', True, False")
        if bad:
          if not error:
            Warning("Received value '%s' of header '%s' does not match pattern '%s'" %(msg[header], header, pattern))
          else:
            self.SeriousError("Received value '%s' of header '%s' does not match pattern '%s', exact match = %s, checkOrder = %s" %(msg[header], header, pattern, exactMatch, checkOrder ))
          return 0
        else:
          PrintLog("\tVerifySIPMsg at dn = %s, EpiID = %s: pattern matches, exact match = %s, checkOrder = %s\n" %(self.phone, sipCallID, exactMatch, checkOrder))
        return 1
          
#----------------------------------------------
  def GetSIPMsgHeader(self, msg, header, sipCallID = None, ps = None, dlg = None, skip = None, error = 1):
    """Calls GetSIP for for specific message
       Raises 'Serious Error' if header is absent.
       parameters
         msg       - specific message, valid  (for EpiPhone's GETSIP) values N|last|name
         header    - string
         sipCallID - int
         ps (a.k.a -PartyState (values:initiated, alerting, connected, held))
         dlg = None|inc|out: most recent incoming/outgoing SIP dialog ID OR 'dev' for query out of call content dialogs
         skip - N parameter to getSIP,X,msg="name" query (to skip N messages from   back of the list matching given name in sip history)
       return:
         header value
    """
    PrintLog("GetSIPMsgHeader at dn = %s, msg = '%s', header = '%s', sipCallID = '%s', ps = '%s', dlg = '%s', skip = '%s':" %(self.phone, msg, header, sipCallID, ps,  dlg, skip))
    code, id, msg = self.GetSIP(sipCallID, msg, ps, dlg, skip, msgAsString = 0)
    header_value = ""
    if not msg.has_key(header):
      self.SeriousError("SIP message does not contain required header '%s'" %header)
    else:
      header_value = msg[header]
      PrintLog('\tGetSIPMsgHeader result at dn = %s, EpiID = %s:\n\t\tHeader = "%s"; Value = "%s"\n---' %(self.phone, sipCallID, header, header_value))
    return header_value
#----------------------------------------------

  def GetLastEpiID(self,dlg = None):
    """
    Parameter:
      dlg = None|inc|out: most recent incoming/outgoing SIP dialog ID
    returns
      most recent incoming (dlg = 'inc')/outgoing  (dlg = 'out') SIP dialog
        If parameter 'dlg' does not present, returns most recent SIP dialog ID
    """
    PrintLog('GetLastEpiID at dn = "%s": dlg = %s' %(self.phone, dlg))
    if dlg:
      code, last_id, msg = self.GetSIP(dlg = dlg)
    else:
      code, last_id, msg = self.GetSIP(dlg = 'inc')
      code, out_id, msg = self.GetSIP(dlg = 'out')
      if out_id > last_id:
        last_id = out_id
    PrintLog("\tGetLastEpiID result at dn = %s: id = %s\n---" %(self.phone, last_id))
    return last_id
#----------------------------------------------

  def SetDefaultMethodDTMF(self, method=None):
    """
    Sets default DTMF method to use by this SipPhone instanse
    
    Arguments:
        method - string or None. Valid values are:
            'rfc2833' - default method will be send DTMF via payload
            'tone' - default method will be send DTMF in-band
            'info' - default method will be send DTMF via SIP INFO
            None - reset default value to default value.

    """
    PrintLog("SipPhone: '%s': Setting defaultMethodDTMF to '%s'" % (str(self.phone), str(method)))
    if not method:
      self.defaultMethodDTMF = 'rfc2833'
    else:
      self.defaultMethodDTMF = method


  def CSS(self, sipCallID = None, ps = None, dlg = None, sipScript = None):
    """
    Custom SIP Scripting (CSS)
    Parameters:
      sipCallID | ps | dlg
         dlg=inc|out|next
      sipScript
    """
    if sipScript:
      sipStr = "(%s)"%sipScript
      if dlg:
        request = 'css,dn=%s,dlg=%s,sip=%s\r\n'%(self.phone, dlg, sipStr)
        PrintLog('\n--Send request to EpiPhone: css,dn=%s,dlg=%s,sip=%s'%(self.phone, dlg, sipStr))
      elif ps:
        request = 'css,dn=%s,ps=%s,sip=%s\r\n' %(self.phone,ps,sipStr)
        PrintLog('\n--Send request to EpiPhone: css,dn=%s,ps=%s,sip=%s'%(self.phone, ps, sipStr))
      elif sipCallID:
        request = 'css,id=%s,sip=%s\r\n' %(sipCallID,sipStr)
        PrintLog('\n--Send request to EpiPhone: css,id=%s,sip=%s'%(sipCallID, sipStr))
      else:
        request = 'css,dn=%s,sip=%s\r\n'%(self.phone, sipStr)
        PrintLog('\n--Send request to EpiPhone: css,dn=%s,sip=%s'%(self.phone, sipStr))
      self.phoneClient().Send(request, printTo = self.printTo)
      response = self.phoneClient().Wait(printTo = self.printTo)
      if not response:
           
        self.SeriousError("Bad result on %s on request %s to EpiPhone (no response)" %(dnName, request), forceReset = 1)   
      PrintLog('  CSS at dn = "%s": %s' %(self.phone, response))
    else:
      PrintLog('  CSS at dn = "%s": Epi-ctrl: invalid Syntax' %self.phone)
      self.SeriousError('CSS at dn = "%s": Epi-ctrl: invalid command' %self.phone)
      
  def GetSIP(self, sipCallID = None, msg = None, ps = None, dlg = None, skip = None, pipe = None, msgAsString = 0, find = ""):
    """Send request getsip to EpiPhone, waits for response
       parameters
          sipCallID - int or str
          msg - str, message to retrieve, msg=M|last|"name"
          ps - str, to be parsed on test level
          dlg = None|inc|out: most recent incoming/outgoing SIP dialog ID OR 'dev' for query out of call content dialogs
          pipe - str
          find - str like ">>='.*'" 
          skip - N parameter to getSIP,X,msg="name" query (to skip N messages from   back of the list matching given name in sip history)
       return
          (code, id, msg) - code - int, call id - int, msg - string (SIP history OR SIP Message)
    """
    msgToGet = msg
    dlgStr = ""
    idStr = ""
    psStr = ""
    msgStr = ""
    pipeStr = ""
    findStr = ""
    skipStr = ""
    if skip:
      skipStr = ",skip=%s"%skip 
    if dlg:
      dlgStr = ",dlg=%s"%dlg 
    if msg:
      msgStr = ",msg=%s"%msg 
    if ps:
      psStr = ",ps=%s"%ps
    if pipe:
      pipeStr = ",pipe=%s"%pipe
    if find:
      findStr = ",find=(%s)"%find
    if sipCallID:
      idStr = ",id=%s"%sipCallID
      request = 'getsip%s%s%s\r\n' %(idStr, msgStr, skipStr)
#      PrintLog('\nSend request to EpiPhone: getsip%s%s'  %(idStr, msgStr))
    elif pipe:
      request = 'getsip%s%s%s%s%s%s\r\n' %(pipeStr, psStr, msgStr, dlgStr, findStr, skipStr)
    else:
      request = 'getsip,dn="%s"%s%s%s%s\r\n' %(self.phone, psStr, msgStr, dlgStr, skipStr)
#      PrintLog('\n---Send request to EpiPhone: getsip,dn="%s"%s%s%s'  %(self.phone, msgStr, psStr,dlgStr))
    PrintLog("\n---Send request to EpiPhone %s" %request.rstrip())
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    PrintLog("   %s" %response.rstrip())
    code, id, msg = self.parseGetSIPResponse(request, response)

    if msgAsString:
      msgStr = str(msg)
      return msgStr
#    PrintLog("    Result on request: Code = %s, Id = %s, Message = %s" %(code, id, msgStr))
    return code, id, msg
  
  

#----------------------------------------------

  
#---------------------------------------------------------------------------------------------------------------------------
# SipPhoneEpi - End Point that can make calls. Inherits all GetSIP functionality from SipPhoneEpiCommon
#---------------------------------------------------------------------------------------------------------------------------
 
class SipPhoneEpi(SipPhoneEpiCommon):
  
  def __init__(self, tDN, host = None, port = 0):
    """parameters:
        tDN - either DN object, or string (number)
        host - string or None
        port - int or None
    """
    #client
    if type(tDN) == type(""):
      phone = tDN
    else:
      phone = tDN.number      
    SipPhoneEpiCommon.__init__(self, phone, host, port)
    
    if type(tDN) == type(""):
      self.number = tDN
      self.tDN = None
    else:
      self.tDN = tDN
      self.globalName = self.tDN.globalName + " " + self.globalName
      #SetNoUserData(1)
      #self.tDN.tserver.testAttrMask["UserData"] = 0
      self.useLinkTserverEndpoint = False

  def UsualCleanUp(self):
    if self.tDN and hasattr(self.tDN.tserver, "drop_nailedup_after_test")\
      and self.tDN.tserver.drop_nailedup_after_test:
      self.Clear()
  
  def Clear(self):
    DebugPrint ("Epiphone cleanup")
    cmd = 'release,dn="%s"\r\n' %self.phone
    self.phoneClient().Send(cmd, printTo = self.printTo)
    self.phoneClient().Wait(printTo = self.printTo)
    # fix by Vlad Gorelov bound to nailed-up model 02/14/14 fix is made not to fail tests in the pack if one failed
    if hasattr(self,"tDN") and hasattr(self.tDN, "parked"):
        self.tDN.parked = 0
  
  #-----------------------------------------
  # GetSIP - different from Pipe, so has to be defined here
  #-----------------------------------------    
  def GetSIP(self, sipCallID = None, msg = None, ps = None, dlg = None, skip = None, pipe = None, msgAsString = 0, find = ""):
    """Send request getsip to EpiPhone, waits for response
       parameters
          sipCallID - int or str
          msg - str, message to retrieve, msg=M|last|"name"
          ps - str, to be parsed on test level
          dlg = None|inc|out: most recent incoming/outgoing SIP dialog ID OR 'dev' for query out of call content dialogs
          pipe - for compatibility only
          find - str like ">>='.*'" 
          skip - N parameter to getSIP,X,msg="name" query (to skip N messages from   back of the list matching given name in sip history)
       return
          (code, id, msg) - code - int, call id - int, msg - string (SIP history OR SIP Message)
    """
    if pipe:
      return SipPhoneEpiCommon.GetSIP(self, sipCallID, msg, ps, dlg, skip, pipe, msgAsString, find)
    msgToGet = msg
    dlgStr = ""
    idStr = ""
    psStr = ""
    msgStr = ""
    findStr = ""
    skipStr = ""
    if skip:
      skipStr = ",skip=%s"%skip 
    if dlg:
      dlgStr = ",dlg=%s"%dlg 
    if msg:
      msgStr = ",msg=%s"%msg 
    if ps:
      psStr = ",ps=%s"%ps
    if find:
      findStr = ",find=(%s)"%find
    if sipCallID:
      idStr = ",id=%s"%sipCallID
      request = 'getsip%s%s%s\r\n' %(idStr, msgStr, skipStr)
      # request = 'getsip%s%s\r\n' %(idStr, msgStr)
#      PrintLog('\nSend request to EpiPhone: getsip%s%s'  %(idStr, msgStr))
    else:
      request = 'getsip,dn="%s"%s%s%s%s\r\n' %(self.phone, psStr, msgStr, dlgStr, skipStr)
#      PrintLog('\n---Send request to EpiPhone: getsip,dn="%s"%s%s%s'  %(self.phone, msgStr, psStr,dlgStr))
    PrintLog("\n---Send request to EpiPhone %s" %request.rstrip())
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    PrintLog("   %s" %response.rstrip())
    code, id, msg = self.parseGetSIPResponse(request, response)

    if msgAsString:
      msgStr = str(msg)
      return msgStr
#    PrintLog("    Result on request: Code = %s, Id = %s, Message = %s" %(code, id, msgStr))
    return code, id, msg
  
  def GetLastIncSDPMsgNumber(self, sipCallID=None, ps=None, dlg=None, skip=None, pipe=None, find=""):
    """ Gets number of last incoming SDP Message with SDP """
    full_msg_list = self.GetSIP(sipCallID, None, ps, dlg, skip, pipe, 1, find).split(",")
    for i in range(1, len(full_msg_list) + 1):
      if ":SDP" in full_msg_list[-i] and "<<" in full_msg_list[-i]:
        return len(full_msg_list) - i + 1
    PrintLog("Messge is not found")
  
  def SetConfig(self, confStr = None, pipe = 0):
    """Send request config to EpiPhone, waits for response
       Raises 'Serious Error' when EpiPhone returns negative responce
       parameters
          confStr - str, e.g  sip='ring', sip='DN4'
          pipe - for compatibility only
       return
          result
    """
    if pipe:
      return SipPhoneEpiCommon.SetConfig(self,  confStr, pipe)
    idStr = ""
    if confStr:
      idStr = ",%s"%confStr    
    request = 'config,dn="%s"%s\r\n' %(self.phone, idStr)
    PrintLog("\n---Send request to EpiPhone %s" %request.rstrip())
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    if not response:
      self.SeriousError("Bad result on %s on request %s to EpiPhone (no response)" %(self.phone, request), forceReset = 1)
    PrintLog("   %s" %response.rstrip())
    if not re.match('\(200,st=.*',response):
      self.SeriousError('Bad result on request "%s" to EpiPhone: %s'%(request.rstrip(), response.rstrip()), forceReset = 1)
    return response      
    
        
      
  #-----------------------------------------
  # Call related methods
  #-----------------------------------------
  
  def MakeCall(self, dest, waitEvents = True, video = "", call=None):
    """Send request call to EpiPhone, waits for response and tlib events 
       parameters
          dest - SIP_DN (Queue, RP) object or string (number to call)
          waitEvents - if True, TLib event
       return
          cl, id - call returned by DN.MakeCall, id of sip call
    """
    if type(dest) in (type(""), type(u"")):
      numberToCall = str(dest)
    else:
      if dest.dialingNumber:
        numberToCall = dest.dialingNumber
      else:
        if self.tDN.callToExtDN(dest):
          numberToCall = dest.tserver.numberForInboundCall + dest.NumberForExtCall()
        else:
          numberToCall = dest.numberForCall
    videoStr = ',video="%s"' %video if video else ""
    
    request = 'call,dn="%s",to="%s"%s\r\n' %(self.phone, numberToCall, videoStr)
    PrintLog('\nSend request to EpiPhone: %s'  %request)
    time.sleep(self.requestTimout)
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    code, id = self.parseResponse(request, response)
    if waitEvents and self.tDN:
      if hasattr(self.tDN, "parked"):
        self.tDN.one_pcc_request = 1
      if (hasattr(self.tDN, "shared_line") or hasattr(self.tDN, "shared_line_number")) and dest == self.tDN:
        sharedLinePtList = call.findSharedLineParties()
        self.tDN.one_pcc_request = 1
        cl = self.tDN.PrivateService(3025, call=call, byDefault=1)
      else:
        cl = self.tDN.MakeCall(dest, userData={}, byDefault=1)
      return cl, id
    return id
  
  
  def AnswerCall(self, sipCallID = None, waitEvents = True, call = None, video = ""):
    """Send request answer to EpiPhone, waits for response and tlib events 
       parameters
          sipCallID - int, id of sip call
       return
          cl, id - call returned by DN.AnswerCall, id of sip call
    """
    id = sipCallID
    #fix by Vlad Gorelov 09/24/13. support of backward compatibility of nailed-up model
    park = 0
    if self.tDN:
        if hasattr(self.tDN, "parked"):
            if InTrue(self.tDN.parked):
                park=1
    #end of fix
    if not self.tDN or (InFalse(self.tDN.autoAnswer) and (not park)) :
      #fix by Vlad Gorelov. added processing of self.tDN.parked flag
      idStr = ""
      if sipCallID:
        idStr = ",id=%s"%sipCallID    
      videoStr = ',video="%s"' %video if video else ""
       
      request = 'answer,dn="%s"%s%s\r\n' %(self.phone, idStr, videoStr)
      PrintLog('\nSend request to EpiPhone: %s'  %request)
      time.sleep(self.requestTimout)
      self.phoneClient().Send(request, printTo = self.printTo)
      response = self.phoneClient().Wait(printTo = self.printTo)
      code, id = self.parseResponse(request, response)
    if waitEvents and self.tDN:
      if hasattr(self.tDN, "parked"):
        self.tDN.one_pcc_request = 1  #fix by Vlad Gorelov 08/05/13. this string indicates that we make 1pcc Answer
      cl = self.tDN.AnswerCall(call, byDefault = 1)
      return cl, id
    return id
    
  def ReleaseCall(self, sipCallID = None, waitEvents = True, call = None):
    """Send request release to EpiPhone, waits for response and tlib events 
       parameters
          sipCallID - int, id of sip call
       return
          cl, id - call returned by DN.ReleaseCall, id of sip call
    """       
    idStr = ""
    if sipCallID:
      idStr = ",id=%s"%sipCallID   
    request = 'release,dn="%s"%s\r\n' %(self.phone, idStr)
    PrintLog('\nSend request to EpiPhone: release,dn="%s"%s' %(self.phone, idStr))
    time.sleep(self.requestTimout)
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    code, id = self.parseResponse(request, response)
    if waitEvents and self.tDN:
      if not ((hasattr(self.tDN, "shared_line") and self.tDN.shared_line) or
              (hasattr(self.tDN, "shared_line_number") and 
                  self.tDN.shared_line_number)):
        self.tDN.abandPermitedOnReleasingInRinging = 1
      if self.tDN.tserver.switchType.name in ("CFGAlcatelA4400DHS3"):
        self.tDN.tserver.retrievedAfterRelOnConsultOrig = 1
      #if self.tDN.line_type == "1":
      #  self.tDN.parked = 0           # fix by Vlad Gorelov 07/11/13
      if hasattr(self.tDN, "parked"):
        self.tDN.one_pcc_request = 1    # fix by Vlad Gorelov 08/05/13 this string indicates that we Make 1pcc Release
      cl = self.tDN.ReleaseCall(call, byDefault = 1)
      self.tDN.abandPermitedOnReleasingInRinging = 0
      return cl, id
    return id

  def HoldCall(self, sipCallID = None, waitEvents = True, call = None):
    """Send request hold to EpiPhone, waits for response and tlib events 
       parameters
          sipCallID - int, id of sip call
       return
          cl, id - call returned by DN.HoldCall, id of sip call
    """        
    idStr = ""
    if sipCallID:
      idStr = ",id=%s"%sipCallID
    request = 'hold,dn="%s"%s\r\n' %(self.phone, idStr)
    PrintLog('\nSend request to EpiPhone: hold,dn="%s"%s' %(self.phone, idStr))
    time.sleep(self.requestTimout)
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    code, id = self.parseResponse(request, response)
    if waitEvents and self.tDN:
      cl = self.tDN.HoldCall(call, byDefault = 1)
      return cl, id
    return id
    
  def RetrieveCall(self, sipCallID = None, waitEvents = True, call = None):
    """Send request retrieve to EpiPhone, waits for response and tlib events 
       parameters
          sipCallID - int, id of sip call
       return
          cl, id - call returned by DN.RetrieveCall, id of sip call
    """        
    idStr = ""
    if sipCallID:
      idStr = ",id=%s"%sipCallID
    request = 'retrieve,dn="%s"%s\r\n' %(self.phone, idStr)
    PrintLog("Send request to EpiPhone %s" %request)
    time.sleep(self.requestTimout)
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    code, id = self.parseResponse(request, response)
    if waitEvents and self.tDN:
      cl = self.tDN.RetrieveCall(call, byDefault = 1)
      return cl, id
    return id
    
  def RedirectCall(self, dest, sipCallID = None, waitEvents = True, call = None):
    """parameters
          dest - SIP_DN (Queue, RP) object
          sipCallID - int, id of sip call (held)
          waitEvents - if True, TLib event
       return
          cl, id - call returned by DN.RedirectCall, id of sip call
    """
    if type(dest) == type(""):
      numberToCall = dest
    else:    
      if self.tDN.callToExtDN(dest):
        numberToCall = dest.tserver.numberForInboundCall + dest.NumberForExtCall()
      else:
        numberToCall = dest.numberForCall
    idStr = ""
    if sipCallID:
      idStr = ",id=%s"%sipCallID
    request = 'css,dn="%s"%s,sip=(302=(to="%s"))\r\n' %(self.phone, idStr, numberToCall)
    
    PrintLog("\nSend request to EpiPhone %s" %request)
    time.sleep(self.requestTimout)
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    code, id = self.parseResponse(request, response)
    if waitEvents and self.tDN:
      cl = self.tDN.RedirectCall(dest, call, callState = CallState.Forwarded, byDefault = 1)
      return cl, id
    return id
  
  def InitiateTransfer(self, dest, sipCallID = None, waitEvents = True, video = ""):
    """parameters
          dest - SIP_DN (Queue, RP) object
          sipCallID - int, id of sip call (held)
          waitEvents - if True, TLib event
       return
          cl, id - call returned by DN.InitateTransfer, id of sip call
    """
    if type(dest) in (type(""), type(u"")):
      numberToCall = str(dest)
    else:    
      if dest.dialingNumber:
        numberToCall = dest.dialingNumber
      else:
        if self.tDN.callToExtDN(dest):
          numberToCall = dest.tserver.numberForInboundCall + dest.NumberForExtCall()
        else:
          numberToCall = dest.numberForCall
    idStr = ""
    if sipCallID:
      idStr = ",id=%s"%sipCallID      
    videoStr = ',video="%s"' %video if video else ""
    
    request = 'startXfer,dn="%s"%s,to="%s"%s\r\n' %(self.phone, idStr, numberToCall, videoStr)
    PrintLog("\nSend request to EpiPhone %s" %request)
    time.sleep(self.requestTimout)
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    code, id = self.parseResponse(request, response)
    if waitEvents and self.tDN:
      cl = self.tDN.InitiateTransfer(dest, userData = {}, byDefault = 1)
      return cl, id
    return id
  
  def CompleteTransfer(self, sipCallID = None, waitEvents = True):
    """parameters
          sipCallID - int, id of sip call (held)
          waitEvents - if True, TLib event
       return
          cl, id - call returned by DN.CompleteTransfer, id of sip call
    """    

    idStr = ""
    if sipCallID:
      idStr = ",id=%s"%sipCallID      
    request = 'transfer,dn="%s"%s\r\n' %(self.phone, idStr)
    PrintLog("\nSend request to EpiPhone %s" %request)
    time.sleep(self.requestTimout)
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    code, id = self.parseResponse(request, response)
    if waitEvents and self.tDN:
      cl = self.tDN.CompleteTransfer(byDefault = 1)
      return cl, id
    return id  
  
  def SingleStepTransfer(self, dest, sipCallID = None, waitEvents = True, video = ""):
    """parameters
          dest - SIP_DN (Queue, RP) object
          sipCallID - int, id of sip call
          waitEvents - if True, TLib event
       return
          cl, id - call returned by DN.SingleStepTransfer, id of sip call
    """
    if type(dest) in (type(""), type(u"")):
      numberToCall = str(dest)
    else:    
      if dest.dialingNumber:
        numberToCall = dest.dialingNumber
      else:
        if self.tDN.callToExtDN(dest):
          numberToCall = dest.tserver.numberForInboundCall + dest.NumberForExtCall()
        else:
          numberToCall = dest.numberForCall
    idStr = ""
    if sipCallID:
      idStr = ",id=%s"%sipCallID      
    videoStr = ',video="%s"' %video if video else ""

    request = 'blindXfer,dn="%s"%s,to="%s"%s\r\n' %(self.phone, idStr, numberToCall, videoStr)
    PrintLog("\nSend request to EpiPhone %s" %request)
    PrintLog("sleeping %s" %self.requestTimout)
    time.sleep(self.requestTimout)
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    code, id = self.parseResponse(request, response)
    if waitEvents and self.tDN:
      #if (self.tDN.line_type == "1"):
      #  self.tDN.parked = 0
      if hasattr(self.tDN, "parked"):              # fix by Vlad Gorelov 07/11/13
        self.tDN.one_pcc_request = 1           #fix by Vlad Gorelov 08/05/13  this string indicates that we make 1pcc SingleStepTransfer
      pt, cl = self.tDN.getPartyFromCall(None, None)
      if self.tDN.tserver.switchType.name not in ["CFGAlcatelA4400DHS3"]:
        if pt:
          ev = self.tDN.mayBeEvent(EventName.Held, pt, timeout = 3)
          if ev:
            self.tDN.mayBeEvent(EventName.Retrieved, pt, timeout = 3)        
        cl = self.tDN.SingleStepTransfer(dest, byDefault = 1)
      else:
        cl = self.tDN.MuteTransfer(dest, userData = {}, byDefault = 1)  
      return cl, id
    return id    

  
  def SendDTMF(self, digits, sipCallID=None, method=None):
    """Send request SendDTMF to EpiPhone, waits for response 
       parameters
          digits    - string, digits to send
          sipCallID - int, id of sip call, optional          
          method - string or None, method to send DTMF. Valid values are
                    None - defaultMethodDTMF value used
                    'rfc2833' - send digits via rfc2833
                    'info' - send digits via SIP INFO messages
                    'tone' - send digits via in-band tones
       return
          id   - call ID
          
    """      
    idStr = ""
    if sipCallID:
      idStr = ",id=%s"%sipCallID
    if not method:
      DebugPrint("SendDTMF: no 'method' parameter given - using defaultMethodDTMF")
      method = self.defaultMethodDTMF
    if method == "rfc2833":
      request_addition = ""
    elif method == "info":
      request_addition = ",info"
    elif method == "tone":
      request_addition = ",tone"
    else:
      Warning("SendDTMF: Incorrect 'method' parameter value '%s'. Should be in ['rfc2833', 'info', 'tone']" % str(method))
    request = 'dtmf,dn="%s"%s,seq="%s"%s\r\n' %(self.phone, idStr, digits, request_addition)
    PrintLog('\nSend request to EpiPhone: %s' %(request))
    time.sleep(self.requestTimout)
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    code, id = self.parseResponse(request, response)
    return id  

  def TLDR(self, expectedRx = None, timeout = 0, ps = None, sipCallID = None): # VitaliyR: changed order of parameters
    """Send request tldr to EpiPhone, waits for response, compares returned result with expected Rx
       parameters
          expectedRx - string, expected Rx
          ps (a.k.a -PartyState (values:initiated, alerting, connected, held))
          timeout    - int
          sipCallID  - int, id of sip call
       return
          id of active SIP dialog
    """
    PrintLog("\n---TLDR at dn = '%s':  expectedRx = '%s', timeout = %s, ps = %s, sipCallID = %s" %(self.phone, expectedRx, timeout, ps, sipCallID))
    time.sleep(timeout)
    idStr = ""
    psStr = ""
    if sipCallID:
      idStr = ",id=%s"%sipCallID
    psStr = ""
    if ps:
      psStr = ",ps=%s"%ps
    rxStr = ',expectedRx="%s"' %expectedRx if expectedRx else ""
    
    request = 'query,dn="%s"%s%s%s\r\n' %(self.phone, idStr, psStr, rxStr)
    psStr = ""
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    result = self.parseResponseQuery(request, response)
    receivedCode = result["code"]
    receivedRx = result["Rx"]
    receivedPs = result["ps"]
    receivedAc = result["ac"]
    idStr = result["id"]
      
    if expectedRx:
      if not receivedRx: # NoRTP
        receivedRx = "noRTP"

        if receivedRx <> expectedRx:
          Error("Bad receivedRx on %s. Expected %s. Received %s" %(self.phone, expectedRx, receivedRx))
        
      else:
        expectedRx = expectedRx.split(";")
        bad = 0
        for l in expectedRx:
          if l.strip() not in receivedRx:
            bad = 1
            break
        for l in receivedRx:
          if l.strip() not in expectedRx:
            bad = 1
            break
        if bad:
          if receivedRx <> expectedRx:
            Error("Bad receivedRx on %s. Expected %s. Received %s" %(self.phone, expectedRx, receivedRx))
    return idStr
  
  def getTone(self, request):
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    result = self.parseResponseQuery(request, response)
    receivedCode = result["code"]
    receivedRx = result["Rx"]
    receivedPs = result["ps"]
    receivedAc = result["ac"]
    idStr = result["id"]
    return receivedCode, receivedRx, receivedPs, receivedAc, idStr
        
  def compareRx(self, expectedRx, receivedRx):
    if expectedRx:
      if not receivedRx: # NoRTP
        receivedRx = "noRTP"

        if receivedRx <> expectedRx:
          
          return 0
        
      else:
        expectedRx = expectedRx.split(";")
        bad = 0
        for l in expectedRx:
          if l.strip() not in receivedRx:
            bad = 1
            break
        for l in receivedRx:
          if l.strip() not in expectedRx:
            bad = 1
            break
        if bad:
          if receivedRx <> expectedRx:
            
            return 0
    return 1
  
  
  def CheckRx(self, expectedRx = None, timeoutToStabilize = 5, minStabTimeout = 0, timeoutToLast = 0, ps = None, sipCallID = None): 
    """Send request tldr to EpiPhone, waits for response, compares returned result with expected Rx
       parameters
          expectedRx            - string, expected Rx
          timeoutToStabilize    - int, seconds, max timeout to wait before Rx sets up
          minStabTimeout        - int, seconds, timeout  Rx stay stable, if 0 exit after detecting first correct tone
          timeoutToLast         - int, seconds, timeout  Rx to last, if 0 exit after detecting first correct tone
       return
          timestamp             - float, time when expected Rx started
    """
    
    assert(timeoutToStabilize > minStabTimeout)
    PrintLog("\nVerifying Rx on dn = '%s', expected tone = '%s', time to stabilize = %s, min stab time = %s, time to last = %s" %(self.phone, expectedRx, timeoutToStabilize, minStabTimeout, timeoutToLast))
    idStr = ""
    psStr = ""
    request = 'query,dn="%s"\r\n' %(self.phone)
    psStr = ""
    

    received = 0
    oldPrintTo = self.printTo
    self.printTo = 0
    startTimeRx = 0
    startTime = time.time()
    stabilized = 0
    try:
      while time.time() < startTime + timeoutToStabilize:
        startTimeRx = time.time()
        receivedCode, receivedRx, receivedPs, receivedAc, idStr = self.getTone(request)
        if not self.compareRx(expectedRx, receivedRx):
          time.sleep(0.2)
          continue
        else:
          if not minStabTimeout:
            received = 1
            PrintLog( "First correct Rx recieved after %s sec" %(time.time() - startTime))
            break            
          else:
            stabilized = 0
            while 1:
  
              receivedCode, receivedRx, receivedPs, receivedAc, idStr = self.getTone(request)
              if not self.compareRx(expectedRx, receivedRx):
                break
              else:
                if time.time() - startTimeRx - minStabTimeout >= 0:
                  
                  stabilized = 1
                  received = 1
                  PrintLog( "Rx tone '%s' stabilized after %s sec" %(expectedRx, round(time.time() - startTime, 2)))
                  break
                else:
                  if time.time() - startTime - timeoutToStabilize - minStabTimeout > 0:
                    break
                  if time.time() - startTimeRx - minStabTimeout > 0:
                    break                  
                  time.sleep(0.2)
                  continue
                
            if not stabilized:
              continue
            else:
              break
      if minStabTimeout and not stabilized:
        self.Error( "Expected Rx tone '%s' did not stabilized after %s sec" %(expectedRx, round(time.time() - startTime, 2)))
        return  startTimeRx
      else:  
        if not received:
          self.Error("Bad Rx on %s. Expected '%s', Received '%s'" %(self.phone, expectedRx, receivedRx))
          return  startTimeRx
      received = 0
      if not timeoutToLast:
        PrintLog("Matched Rx on %s. " %(self.phone))
        return startTimeRx
      #else - timeoutToLast:
  
      PrintLog("Rx on %s should last %s seconds. Expected tone %s"%(self.phone, timeoutToLast, expectedRx))
      PrintLog("Checking remaining %s seconds" %int(startTimeRx - time.time() + timeoutToLast))
      i = 0
      bad = 0
      warningString = ""
      while time.time() < startTimeRx + timeoutToLast:
        self.phoneClient().Send(request, printTo = self.printTo)
        response = self.phoneClient().Wait(printTo = self.printTo)
        if time.time() >= startTimeRx + timeoutToLast: break
        result = self.parseResponseQuery(request, response)
        receivedCode = result["code"]
        receivedRx = result["Rx"]
        receivedPs = result["ps"]
        receivedAc = result["ac"]
        idStr = result["id"]
        if not self.compareRx(expectedRx, receivedRx):
          if warningString :
            warningString = warningString + "\n     Bad Rx on %s during second %s. Expected %s. Received %s" %(self.phone, i, expectedRx, receivedRx)
          else:
            warningString = "Bad Rx on %s during second %s. Expected %s. Received %s" %(self.phone, i, expectedRx, receivedRx)
          bad = 1
        print "Sec %s. OK" %i
        time.sleep(0.5)
        i += 0.5
      if not bad:
        PrintLog("Matched Rx on %s." %(self.phone))
      else:
        self.Warning(warningString)
      return startTimeRx  
    finally:
      self.printTo = oldPrintTo
      return startTimeRx  
      
  

  
  def WaitPartyState(self, expectedPartyState = None, sipCallID = None, lastID = None, timeout = 5, optional = 0, index = None):
    """Waits for active party to get into specified party state during timeout
    Raises 'Serious Error' if no expected PartyState during timeout
    Parameters: 
       expectedPartyState (values:initiated, alerting, connected, held)
       sipCallID (a.k.a EpiID)
       lastID
       timeout
       index
    Return: 
      Success: EpiID (sipCallID)
      Failure: '0' 
    ------------------------------------------------------------------------------------------------
    Behavior:
    if expectedPartyState:
      if index <> None
        Waits for dialog SPECIFIED by index to get into specified party state during timeout
        -1 means most recent dialog, 0 - first dialog, etc
        Useful if sipCallID is not known but the sequence of dialog creations in known
      else:
        if lastID:
          Waits for NEW (most recent) dialog  to get into specified party state during timeout
        elif sipCallID:
          Waits for SPECIFIED dialog  to get into specified party state during timeout
        else
          Waits for ACTIVE ('code' = 200) dialog to get into specified party state during timeout
    else:
      if sipCallID:
        Waits for SPECIFIED dialog  to get released (481/Call not found for 'Query'/specified id ) during timeout
      else
        Waits for ALL dialogs to get released (481/Call not found for 'QueryAll') during timeout
    
    Notes:
      Primary usage of 'lastID' is for waiting party state 'alerting' to avoid race conditions 
      when several dialogs on given DN are in 'alerting' state...
    Recommendations: 
      Always try to use 'sipCallID' (a.k.a EpiID). For waiting party state 'alerting' to avoid race 
      conditions when several dialogs on given DN are in 'alerting' state - use 'lastID'
      You can get 'lastID' by calling 'GetlastID' on given DN before making test call to it.
    """
#=========================
    startTime = time.time()

    
    dnName = "%s %s" %(self.globalName, self.phone)
    #request = 'query,dn="%s",ps=all\r\n' %self.phone
    PrintLog("\n  Waiting: PartyState '%s' on %s sipCallID = %s, lastID = %s, timeout = %s, optional %s"%(expectedPartyState, dnName, sipCallID, lastID, timeout, optional))
    if expectedPartyState == 'held' and self.useLinkTserverEndpoint:
      optional = 1
    if expectedPartyState:
      errorMsg = "No expected party state '%s' on %s" %(expectedPartyState, dnName)
    else:
      errorMsg = "%s is NOT IDLE" %dnName
    if type(expectedPartyState) == type(""):
      expectedPartyState = (expectedPartyState,)
    dnstate = ""
    while time.time() < startTime + timeout:
      dnstate = ""
      id = 0
      request = 'query,dn="%s",ps=all\r\n' %self.phone
      self.phoneClient().Send(request, printTo = self.printTo)
      firstTime = 1
      QueryAllResp = []
      while 1:
        if firstTime:
          waitTimeout = timeout
        else:
          waitTimeout = 0.1
        resp = self.phoneClient().Wait(printTo = self.printTo, timeout = waitTimeout)
        firstTime = 0
        if not resp: break
        QueryAllResp.append(resp)
        
        
      if not QueryAllResp:
           
        self.SeriousError("Bad result on %s on request %s to EpiPhone (no response)" %(dnName, request), forceReset = 1)    
        

      for dialog in QueryAllResp:
        if dialog:
          result = self.parseResponseQuery(request, dialog)
          dnstate = dnstate + '      ' + str(result) + '\n'
      if index <> None: #dialog is specified not sipCallID or lastID but by index in party list
        try:
          dialog = QueryAllResp[index]

          result = self.parseResponseQuery(request, dialog)
          if result['id'] == '':
            result['id'] = 0          
          if result["ps"] in expectedPartyState:
            id = result['id']
            idQuery = result
            logMsg = '    Dialog (index = %s) in "%s" PartyState on %s:\n      %s'%(index, expectedPartyState, dnName, result)
            break          
        except IndexError:
          pass
      else:    
  
        for dialog in QueryAllResp:

          result = self.parseResponseQuery(request, dialog)
          if result['id'] == '':
            result['id'] = 0
          if expectedPartyState:
            # Waits for NEW (most recent) dialog  to get into specified party state during timeout
            if lastID and int(result['id']) > int(lastID) and result["ps"] in expectedPartyState:
              id = result['id']
              logMsg = '    Most Recent dialog in "%s" PartyState on %s:\n      %s'%(expectedPartyState, dnName, result)
              break
            elif sipCallID and result['id'] == sipCallID and result["ps"] in expectedPartyState:
            # Waits for SPECIFIED dialog  to get into specified party state during timeout
              id = result['id']
              logMsg = '    Dialog (id = %s) in "%s" PartyState on %s:\n      %s'%(id, expectedPartyState, dnName, result)
              break
            else:
            # Waits for ACTIVE dialog to get into specified party state during timeout
              if result['code'] == '200' and result["ps"] in expectedPartyState:
                id = result['id']
                idQuery = result
                logMsg = "    Active dialog in '%s' PartyState on %s:\n      %s"%(expectedPartyState, dnName, result)
                break
          else:
            # Waits for SPECIFIED dialog  to get released (481/Call not found for 'Query'/specified id ) during timeout
            if sipCallID:
              errorMsg = "Dialog (id = %s) on %s IS NOT RELEASED" %(sipCallID, dnName)
              request = 'query,dn="%s",id=%s\r\n' %(self.phone, sipCallID)
              self.phoneClient().Send(request, printTo = self.printTo)
              response = self.phoneClient().Wait(printTo = self.printTo)
              if not response:
                   
                self.SeriousError("Bad result on %s on request %s to EpiPhone (no response)" %(dnName, request), forceReset = 1)    
              
              if response:
                result = self.parseResponseQuery(request, response)
                if result['code'] == '481':
                  logMsg = '    Dialog (id = %s) on %s RELEASED:\n      %s'%(sipCallID, dnName, result)
                  id = sipCallID
                  break
            else:
              if result['code'] == '481':
                logMsg = '    %s is IDLE:\n      %s'%(dnName, result)
                id = 1
                break
      if id: break
      time.sleep(0.1)
    PrintLog('    QueryAll for %s:\n%s'%(dnName, dnstate))
    if id:
      PrintLog(logMsg)
      return id
    if result:
      errorMsg = errorMsg + "\n     Received %s"%result
    if not optional:
      
      self.SeriousError(errorMsg) 
    return id

  
#----------------------------------------------
  def SUBSCRIBE(self, headers=None, content=None, to=None, revert=0, event=None):
    """dynamically changes SIP configuration of endpoint with provided headers in paramenters,
       send request to EpiPhone to perform subscribe and reverts configuration 
       Raises 'Serious Error' if 'sipsub' is failed.
       parameters
         headers  - string, dynamically changes dn sip configuration, specifies 'sip-subscribe-headers' (custom headers to be added to SUBSCRIBE message) in format
                    "header"="value" divided by comas
                      example: 'Event="generic-package-1",Accept="format-1,format-2,format-3"'
         content  - string, dynamically changes dn sip configuration, specifies 'sip-subscribe-content' - optional content of the message (in format "type"="body", lines in body separated with '|')
                       example: "text/plain" = "line1|line2"
         to  - string, dynamically changes dn sip configuration, specifies 'sip-subscribe-to' - DN (user) to subscribe to (this DN if not specified)

         revert - if set to '1' - reverts EpiPhone's DN configuration to file values after execution
         event - contents of Event header(designed for shared line, proper values: "call-info" or "line-seize")
    """
    
    if content:
      epiCfgUpdate = 'sip-subscribe-content=(' + content + ')'
      self.SetConfig(epiCfgUpdate)
    if headers:
      epiCfgUpdate = 'sip-subscribe-headers=(' + headers + ')'
      self.SetConfig(epiCfgUpdate)
    if to:
      epiCfgUpdate = 'sip-subscribe-to=\"' + to + '\"'
      self.SetConfig(epiCfgUpdate)
    if event:
        request = 'sipsub,dn="%s",event="%s"\r\n' % (self.phone, event)
    else:
        request = 'sipsub,dn="%s"\r\n'%self.phone
    
    request = 'sipsub,dn="%s"\r\n'%self.phone
    
    PrintLog("\n---Send request to EpiPhone %s" %request.rstrip())
    
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    
    PrintLog("   %s"%response.rstrip())

    if revert:
      self.SetConfig('revert')
    
    if not re.match('\(200,st="subscribing"\)',response):
      self.SeriousError('Bad result on request "%s" to EpiPhone: %s'%(request.rstrip(), response.rstrip()))
#----------------------------------------------    
  def UNSUBSCRIBE(self, revert=0, event=None):
    """Sends sip SUBSCRIBE with Expires=0 for existed subscription
       Raises 'Serious Error' if 'sipunsub' is not sent.
       parameter
         revert - if set to '1' - reverts EpiPhone's DN configuration to file values after execution
         event - contents of Event header(designed for shared line, proper values: "call-info" or "line-seize")
    """

    if event:
        request = 'sipunsub,dn="%s",event="%s"\r\n' % (self.phone, event)
    else:
        request = 'sipunsub,dn="%s"\r\n'%self.phone

    PrintLog("\n---Send request to EpiPhone %s" %request.rstrip())

    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)

    PrintLog("   %s"%response.rstrip())

    if revert:
      self.SetConfig('revert')

    if not re.match('\(200,st="unsubscribing"\)',response):
      self.SeriousError('Bad result on request "%s" to EpiPhone: %s'%(request.rstrip(), response.rstrip()))
#----------------------------------------------

  def REGISTER(self, headers = None, revert = 0, registrar = None):
    """dynamically changes SIP configuration of endpoint (if parameters provided),
       Raises 'Serious Error' if 'sipreg' returns negative response.
       parameters
         headers  - string, dynamically changes dn sip configuration, specifies 'sip-register-headers' (custom headers to be added to REGISTER message)
                    example: 'sip-register-headers = (X-Ringing-Header="custom register header value")'
         revert - if set to '1' - reverts EpiPhone's DN configuration to file values after execution
         registrar -  Valid values:primary, backup (case-insensitive).
                      Parameter makes sense when both sip-proxy and sip-proxy-backup are configured on siie where DN is located
                      When parameter is omitted or contains not matched with any of valid values string - registration is sent to
                      both sip proxies.
    """
    reg = ""
    if registrar  and re.match('primary$',registrar, re.I):
      reg = ", reg=1"
    if registrar  and re.match('backup$',registrar, re.I):
      reg = ", reg=2"
      
    if headers:
      epiCfgUpdate = 'sip-register-headers=(' + headers + ')'
      self.SetConfig(epiCfgUpdate)
    
    request = 'sipreg,dn="%s"%s\r\n'%(self.phone, reg)

    PrintLog("\n---Send request to EpiPhone: %s" %request.rstrip())

    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    
    PrintLog("   %s" %response.rstrip())

    if revert:
      self.SetConfig('revert')
    
    if not re.match('\(200,st="registering"\)',response):
      self.SeriousError('Bad result on request "%s" to EpiPhone: %s'%(request.rstrip(), response.rstrip()))
#----------------------------------------------    

  def UNREGISTER(self, revert = 0, registrar = None):
    """Sends sip REGISTER with Expires=0 for existed registration sip dialog
       Raises 'Serious Error' if 'sipunreg' returns negative response.
       parameter:
         revert - if set to '1' - reverts EpiPhone's DN configuration to file values after execution
         registrar -  Valid values:primary, backup (case-insensitive).
                      Parameter makes sense when both sip-proxy and sip-proxy-backup are configured on siie where DN is located
                      When parameter is omitted or contains not matched with any of valid values string - registration is sent to
                      both sip proxies.
    """
    reg = ""
    if registrar  and re.match('primary$',registrar, re.I):
      reg = ", reg=1"
    if registrar  and re.match('backup$',registrar, re.I):
      reg = ", reg=2"
    request = 'sipunreg,dn="%s"%s\r\n'%(self.phone, reg)
    PrintLog("\n---Send request to EpiPhone: %s" %request.rstrip())

    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)

    PrintLog("   %s" %response.rstrip())

    if revert:
      self.SetConfig('revert')

    if not re.match('\(200,st="unregistering"\)',response):
      self.SeriousError('Bad result on request "%s" to EpiPhone: %s'%(request.rstrip(), response.rstrip()))

#----------------------------------------------    
  def NOTIFY(self, msg = None, revert = 0):
    """Send sip NOTIFY, requires client-side subscription active (i.e. SIP Server should be configured to send SUBSCRIBE to EpiPhone
       Raises 'Serious Error' if 'SIPntfy' returns negative response.
       parameters:
         msg - simple-msg or presence NOTIFY. Valid names are defined by 'on-subscribe' option for server-side subscription
           which are referred to names defined by option 'on-subscribe', for example:
           on-subscribe=(accept="presence",init=p.cisco.open,busy=p.cisco.busy,idle=p.cisco.open,term=p.term)
         revert - if set to '1' - reverts EpiPhone's DN configuration to file values after execution
    """
    request = 'sipntfy,dn="%s", msg = "%s"\r\n'%(self.phone, msg)
    PrintLog("\n---Send request to EpiPhone: %s" %request.rstrip())

    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)

    PrintLog("   %s" %response.rstrip())


    if not re.match('\(200,st="ok"\)',response):
      self.SeriousError('Bad result on request "%s" to EpiPhone: %s'%(request.rstrip(), response.rstrip()))

    if revert:
      self.SetConfig('revert')
#----------------------------------------------

  def PUBLISH(self, msg = None, config = None, to = None, revert = 0):
    """Send sip PUBLISH, requires predefined section in EpiPhone configuration
       Raises 'Serious Error' if 'sippub' returns negative response.
       parameter:
         config - string, dynamically changes dn sip configuration, defines list of 'activities' for PUBLISH in format
                       <name-of-activity>=<name-of-section-in-config-file>, for example:
                           sip-publish = (make-busy=p.on-the-phone,refresh=p.refresh,idle=p.remove)
         to  - string, dynamically changes dn sip configuration, specifies DN (user) to subscribe to (this DN if not specified)
               example: sip-publish-to = "3002"
         msg - any names of presence state defined by 'sip-publish' option
         
         revert - if set to '1' - reverts EpiPhone's DN configuration to file values after execution
    """
    if config:
      epiCfgUpdate = 'sip-publish=(' + config + ')'
      self.SetConfig(epiCfgUpdate)
    if to:
      epiCfgUpdate = 'sip-publish-to=\"' + to + '\"'
      self.SetConfig(epiCfgUpdate)
    request = 'sippub,dn="%s", msg = "%s"\r\n'%(self.phone, msg)
    PrintLog("\n---Send request to EpiPhone: %s" %request.rstrip())

    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)

    PrintLog("   %s" %response.rstrip())


    if not re.match('\(200,st="ok"\)',response):
      self.SeriousError('Bad result on request "%s" to EpiPhone: %s'%(request.rstrip(), response.rstrip()))

    if revert:
      self.SetConfig('revert')
     
      
  def MESSAGE(self, dest, msg=None):
    """Send sip MESSAGE
       Raises 'Serious Error' if 'sipmsg' returns negative response.
       parameter:
         dest - SIP_DN, object
         msg - text message
    """
    if type(dest) in (str, unicode):
        numberToCall = str(dest)
    else:
        if dest.dialingNumber:
            numberToCall = dest.dialingNumber
        else:
            if self.tDN.callToExtDN(dest):
                numberToCall = dest.tserver.numberForInboundCall + dest.NumberForExtCall()
            else:
                numberToCall = dest.numberForCall
    request = 'sipmsg,dn="%s", to="%s", msg="%s"\r\n'%(self.phone, numberToCall, msg)
    PrintLog("\n---Send request to EpiPhone: %s" %request.rstrip())

    self.phoneClient().Send(request, printTo=self.printTo)
    response = self.phoneClient().Wait(printTo=self.printTo)

    PrintLog("   %s" %response.rstrip())

    if not re.match('\(200,st="ok"\)', response):
        self.SeriousError('Bad result on request "%s" to EpiPhone: %s'%(request.rstrip(), response.rstrip()))

#End SipPhone Epi Methods


#-----------------------------------------
# SipPhoneEpiPipe - Pipe (cannot make calls, only GetSIP related things)
#-----------------------------------------
class SipPhoneEpiPipe(SipPhoneEpiCommon):
  
  def __init__(self, tDN, host = None, port = 0):
    """parameters:
        tDN - either DN object, or string (number)
        host - string or None
        port - int or None
    """

    if type(tDN) == type(""):
      phone = tDN
      self.tDN = None
    else:
      self.tDN = tDN
      phone = tDN.number      
    SipPhoneEpiCommon.__init__(self, phone, host, port)
    
    self.pipeName = phone
    self.globalName = "EpiPipe %s"%self.pipeName
    

    
  #no parameter pipe here!  
  def GetSIP(self, sipCallID = None, msg = None, ps = None, dlg = None, skip = None, msgAsString = 0, find = ""):
    """Send request getsip to EpiPhone, waits for response
       parameters
          sipCallID - int or str
          msg - str, message to retrieve, msg=M|last|"name"
          ps - str, to be parsed on test level
          dlg = None|inc|out: most recent incoming/outgoing SIP dialog ID OR 'dev' for query out of call content dialogs
          find - str like ">>='.*'" 
          skip - N parameter to getSIP,X,msg="name" query (to skip N messages from   back of the list matching given name in sip history)
       return
          (code, id, msg) - code - int, call id - int, msg - string (SIP history OR SIP Message)
    """
    msgToGet = msg
    dlgStr = ""
    idStr = ""
    psStr = ""
    msgStr = ""
    findStr = ""
    skipStr = ""
    if skip:
      skipStr = ",skip=%s"%skip 
    if dlg:
      dlgStr = ",dlg=%s"%dlg 
    if msg:
      msgStr = ",msg=%s"%msg 
    if ps:
      psStr = ",ps=%s"%ps
    if find:
      findStr = ",find=(%s)"%find
    if sipCallID:
      idStr = ",id=%s"%sipCallID
      request = 'getsip%s%s%s\r\n' %(idStr, msgStr, skipStr)
#      PrintLog('\nSend request to EpiPhone: getsip%s%s'  %(idStr, msgStr))
    else:
      request = 'getsip,pipe="%s"%s%s%s%s\r\n' %(self.pipeName, psStr, msgStr, dlgStr, skipStr)
#      PrintLog('\n---Send request to EpiPhone: getsip,dn="%s"%s%s%s'  %(self.phone, msgStr, psStr,dlgStr))
    PrintLog("\n---Send request to EpiPhone %s" %request.rstrip())
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    PrintLog("   %s" %response.rstrip())
    code, id, msg = self.parseGetSIPResponse(request, response)

    if msgAsString:
      msgStr = str(msg)
      return msgStr
#    PrintLog("    Result on request: Code = %s, Id = %s, Message = %s" %(code, id, msgStr))
    return code, id, msg
  
  #no parameter pipe here!  
  def SetConfig(self, confStr = None):
    """Send request config to EpiPhone, waits for response
       Raises 'Serious Error' when EpiPhone returns negative responce
       parameters
          confStr - str, e.g  sip='ring', sip='DN4'
       return
          result
    """
    idStr = ""
    if confStr:
      idStr = ",%s"%confStr    
    request = 'config,pipe="%s"%s\r\n' %(self.pipeName, idStr)
    PrintLog("\n---Send request to EpiPhone %s" %request.rstrip())
    self.phoneClient().Send(request, printTo = self.printTo)
    response = self.phoneClient().Wait(printTo = self.printTo)
    if not response:
      self.SeriousError("Bad result on %s on request %s to EpiPhone (no response)" %(self.phone, request), forceReset = 1)
    
    PrintLog("   %s" %response.rstrip())
    if not re.match('\(200,st=.*',response):
      self.SeriousError('Bad result on request "%s" to EpiPhone: %s'%(request.rstrip(), response.rstrip()), forceReset = 1)
    return response   
