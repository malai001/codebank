from xml.dom import minidom as DOM

import os
import re


class XML_Parser():
	'''This class is used to parse the xml files'''

	def __init__(self, file_name, proj_base_path):

		self.file_name = file_name
		self.file_path = ""

		if not proj_base_path:
			print "Project base path argument should not be blank"
		self.proj_base_path  = os.path.abspath(proj_base_path)
		if not os.path.exists(self.proj_base_path):
			print "Project base path %s not exists on the system" % self.proj_base_path
		if file_name:
			#print file_name
			self.file_path = self.findFilePath()
		else:
			print "file name argument should not be blank"

	def __str__(self):

		str_obj = "=========%s Object Instance Values===============\n" % self.__class__.__name__
		str_obj += "file name %s\n" % self.file_name
		str_obj += "file Path %s\n" % self.file_path
		str_obj += "Project Base Path%s\n" % str(self.proj_base_path)
		str_obj += "==============================================\n"
		return str_obj

	def findFilePath(self):
		'''This function walk through the base_path dictory and return the full path of expected file'''
		if self.file_name:
			if self.proj_base_path:
				for root, dirs, files in os.walk(self.proj_base_path):
					for file_ in files:
						if self.file_name == file_:
							self.proj_base_path = os.path.dirname(root)#get project path
							return os.path.join(root,file_)
				else:
					print " %s File is not found in the directory %s" % (self.file_name,str(self.proj_base_path))
			else:
				print "Project base path is empty"
		else:
			print "Empty file name"


	def getValueFromXML(self, find_tag, attr_name="", id_tag="", id_attr_name="", id_attr_val="",
						is_text=0, serious_error=1):
		if self.file_path:
			base_path = self.file_path
		elif serious_error:
			print "File path is empty"
		else:
			return 0
		
		with open(base_path, "r") as f:
			tree = DOM.parse(f)
			
		if id_tag:
			found = 0
			attr_list = []
			tag_list = tree.getElementsByTagName(id_tag)
			for tag in tag_list:
				if tag.hasAttribute(id_attr_name) and tag.attributes[id_attr_name].value == id_attr_val:
					tree = tag
					# print "ID tag and attributes are matching\n",tree.toprettyxml()
					found = 1
					break
			if not found:
				if serious_error:
					for tag in tag_list:
						print "\n",tag.toprettyxml()
					print "***************************************************"
					print self.file_path
					print "***************************************************"
					print "Error: Id tag is not found or attributes are invalid\n\id_tag %s \t id_attr_name %s \t id_attr_val %s" % (id_tag,id_attr_name,id_attr_val)
				else:
					return 0
			tag_list = tree.getElementsByTagName(find_tag)
			for tag in tag_list:
				if attr_name:
					if tag.hasAttribute(attr_name):
						attr_list.append(tag.attributes[attr_name].value)
				elif is_text:
					print tag.firstChild.nodeValue
					return tag.firstChild.nodeValue	
				else:
					return tag.attributes.items()
			else:
				if attr_list:
					return attr_list
				elif serious_error:
					for tag in tag_list:
						print "\n",tag.toprettyxml() 
					print "Error: %s tag or %s attribute is not found" % (find_tag,attr_name)
				else:
					return 0
		else:
			attr_list = []
			tag_list = tree.getElementsByTagName(find_tag)
			for tag in tag_list:
				if id_attr_name and id_attr_val:
					cond = tag.hasAttribute(id_attr_name) and tag.attributes[id_attr_name].value == id_attr_val
					if cond:
						if attr_name and tag.hasAttribute(attr_name):
							attr_list.append(tag.attributes[attr_name].value)
						else:
							return tag.attributes.items()
				elif attr_name:
					if tag.hasAttribute(attr_name):
						attr_list.append(tag.attributes[attr_name].value)
				elif is_text:
					return tag.firstChild.nodeValue
				else:
					return tag.attributes.items()
			else:
				if attr_list:
					return attr_list
				elif serious_error:
					for tag in tag_list:
						print "\n",tag.toprettyxml() 
					print "Error: %s tag or %s attribute is not found" % (find_tag,attr_name)
				else:
					return 0
#def custom_parse():
#def Extract_Var_Value(attr_dic,screen_key_list,parse_obj):
#	'''This function is used to extract variable value from Entry block'''
#	for key in screen_key_list:
#		if key in attr_dic:
#			var_val = get_Var_Value(attr_dic[key],parse_obj)
#			if var_val:
#				attr_dic[key] = var_val
#	return attr_dic
def get_Var_Value(var_name,obj,block_name="Entry1",isDict=0):

	var_s = obj.getValueFromXML("script",is_text=1,id_tag="state",id_attr_name="id",id_attr_val=block_name)
	#print "key value\n",var_name
	#print "variable list\n",var_s
	if var_s and var_name in var_s:
		if isDict:
			pattern = '''[\'\"]{0}[\'\"]\s*:\s*[\'\"](.*?)[\'\"][,\n]'''.format(var_name)
		else:
			pattern = '''{0}\s*=\s*[\'\"](.*?)[\'\"];'''.format(var_name)
		match = re.search(pattern,var_s)
		if match:
			return match.group(1)
		else:
			print "could not fetch variable value"
	else:
		print "variable could not get from script tag"		

def Qaart_Verification(CallingListData,id_attr_val1):
#	print CallingListData
	parser = XML_Parser("default11.scxml","C:\Python27\example") 
#	script_data =  parser.getValueFromXML("script",is_text=1,id_tag="state",id_attr_name="id",id_attr_val="AddRecord1", serious_error=0)
#	print script_data
#	pattern = '''\w+\[\'\w+\'\]\[\'(.*)\'\]\s*=\s*\'*(.*?)\'*;'''
#	key =[]
#	data = []
#	data_n = {}
#	it = re.finditer(pattern,script_data)
#	for match in it:
#		data.append(match.group(2))
#		key.append(match.group(1))
#		data_n[match.group(1)]=match.group(2)
#	print data
#	print key
#	print data_n
#	dic = {}
#	i=0
#	#l=0
#	k = get_Var_Value(data[7],parser)
#	print data[7]
#	if k == '23:59':
##	data[7] = k
#	data_n[key[7]] = k
#	Call_Result_val_dic = { 'Abandoned':'21' ,'Agent CallBack Error':'47' ,'All Trunks Busy':'10','Answer':'33','Cancel Record':'52','Answering Machine Detected':'9', 'Bridged':'31','Busy':'6','Call Drop Error':'42','Cleared':'19','Conferenced':'2','Consult':'24','Converse-On':'30','Covered':'29','Deafened':'49','Dial Error':'41','Do Not Call':'51','Dropped':'26','Dropped on No Answer':'27','Fax Detected':'17','Held':'50','Forwarded':'23','General Error':'3','Group Callback Error':'48','No Dial Tone':'35','No Established Detected':'38','No Port Available':'44','No Progress':'36','No RingBack Tone':'37','NU Time':'34','OK':'0','Overflowed':'20','Pager Detected':'39','Pickedup':'25','Queue Full':'18','Redirected':'22','Remote Release':'5','Silence':'32','SIT Detected':'8','SIT IC (Intecepted)':'13','SIT Invalid Number':'11','SIT NC (No Circuit)':'15','SIT RO (Reorder)':'16','SIT Unknown Call State':'14','SIT VC (Vacant Code)':'12','Stale':'46','Switch Error':'43','System Error':'4','Transfer Error':'45','Transferred':'1','Unknown Call Result':'28','Wrong Number':'53','Wrong Party':'40'}
	#phone_type_dic = {'Modem':'7','Voice Mail':'8','Pin Pager':'9'}
	#for l in range(len(data)):
	#	try:
	#		chkr = phone_type_dic.keys()[phone_type_dic.values().index(data[l])]
	#		print chkr
	#		if chkr:
	#			data[l]= chkr
	#			data_n[key[l]]= chkr
				#key[l] = Call_Result_val_dic[chkr]
	#	except ValueError:
	#		chkr=" "
#	print data
#	print data_n
#	for var in data:
#		try:
#			chk = CallingListData.keys()[CallingListData.values().index(data[i])]	
#			dic[key[i]]=chk;
#
#		except ValueError:
#			chk=" "	
#		i=i+1
#	print dic
#	dic_f = {}
#	for key,value in dic.iteritems():
#		dic_f [value] = data_n[key]
#	print dic_f

#	for key,value in dic_f.iteritems():
#		if dic_f [key] == CallingListData[key]:
#			print "Passed" 
#		else:
#			print "failed"
#parser = XML_Parser("default.scxml",proj_base_path) 
	script_data =  parser.getValueFromXML("script",is_text=1,id_tag="state",id_attr_name="id",id_attr_val=id_attr_val1, serious_error=0)
	print script_data
	pattern = '''\w+\[\'\w+\'\]\[\'(.*)\'\]\s*=\s*\'*(.*?)\'*;'''
	key =[]
	data = []
	data_n = {}
	it = re.finditer(pattern,script_data)
	for match in it:
		data.append(match.group(2))
		key.append(match.group(1))
		data_n[match.group(1)]=match.group(2)
	print data
	#PrintLog(key)
	#PrintLog( data_n)
	dic = {}
	i=0
	#l=0
	#k = get_Var_Value(data[7],parser)
	#print data[7]
	#data[7] = k
	#data_n[key[7]] = k
	Call_Result_val_dic = { 'Abandoned':'21' ,'Agent CallBack Error':'47' ,'All Trunks Busy':'10','Answer':'33','Cancel Record':'52','Answering Machine Detected':'9', 'Bridged':'31','Busy':'6','Call Drop Error':'42','Cleared':'19','Conferenced':'2','Consult':'24','Converse-On':'30','Covered':'29','Deafened':'49','Dial Error':'41','Do Not Call':'51','Dropped':'26','Dropped on No Answer':'27','Fax Detected':'17','Held':'50','Forwarded':'23','General Error':'3','Group Callback Error':'48','No Dial Tone':'35','No Established Detected':'38','No Port Available':'44','No Progress':'36','No RingBack Tone':'37','NU Time':'34','OK':'0','Overflowed':'20','Pager Detected':'39','Pickedup':'25','Queue Full':'18','Redirected':'22','Remote Release':'5','Silence':'32','SIT Detected':'8','SIT IC (Intecepted)':'13','SIT Invalid Number':'11','SIT NC (No Circuit)':'15','SIT RO (Reorder)':'16','SIT Unknown Call State':'14','SIT VC (Vacant Code)':'12','Stale':'46','Switch Error':'43','System Error':'4','Transfer Error':'45','Transferred':'1','Unknown Call Result':'28','Wrong Number':'53','Wrong Party':'40'}
	for l in range(len(data)):
		try:
			chkr = Call_Result_val_dic.keys()[Call_Result_val_dic.values().index(data[l])]
			print chkr
			if chkr:
				data[l]= chkr
				data_n[key[l]]= chkr
		except ValueError:
			chkr=" "
	#PrintLog(data)
	for var in data:
		try:
			chk = CallingListData.keys()[CallingListData.values().index(data[i])]	
			dic[key[i]]=chk;

		except ValueError:
			chk=" "	
		i=i+1
	#PrintLog(dic)
	dic_f = {}
	for key,value in dic.iteritems():
		dic_f [value] = data_n[key]
	#PrintLog(dic_f)

	for key,value in dic_f.iteritems():
		if dic_f [key] == CallingListData[key]:
			print "Passed" 
		else:
			print "failed - Wrong Value update in database"	


#CallingListData = [{u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'General', u'record_id': u'403', u'call_result': u'Unknown Call Result', u'daily_till': u'64800', u'group_id': u'', u'chain_id': u'386', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'6505556455', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'28800', u'switch_id': u'', u'tz_dbid': u'IST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'Direct Business Phone', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}]
CallingListData =  [{u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'General', u'record_id': u'592', u'call_result': u'Unknown Call Result', u'daily_till': u'64800', u'group_id': u'', u'chain_id': u'567', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'6505556455', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'28800', u'switch_id': u'', u'tz_dbid': u'IST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'Direct Business Phone', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}, {u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'General', u'record_id': u'593', u'call_result': u'Abandoned', u'daily_till': u'64800', u'group_id': u'', u'chain_id': u'568', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'6505559881', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'28800', u'switch_id': u'', u'tz_dbid': u'IST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'Direct Business Phone', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}, {u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'General', u'record_id': u'594', u'call_result': u'Agent CallBack Error', u'daily_till': u'64800', u'group_id': u'', u'chain_id': u'569', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'6505554872', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'28800', u'switch_id': u'', u'tz_dbid': u'IST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'Direct Business Phone', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}, {u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'General', u'record_id': u'595', u'call_result': u'All Trunks Busy', u'daily_till': u'64800', u'group_id': u'', u'chain_id': u'570', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'6505556455', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'28800', u'switch_id': u'', u'tz_dbid': u'IST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'Direct Business Phone', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}, {u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'General', u'record_id': u'596', u'call_result': u'Answer', u'daily_till': u'64800', u'group_id': u'', u'chain_id': u'571', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'6505559881', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'28800', u'switch_id': u'', u'tz_dbid': u'IST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'Direct Business Phone', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}]

#cldata = [{u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'General', u'record_id': u'309', u'call_result': u'Unknown Call Result', u'daily_till': u'86340', u'group_id': u'', u'chain_id': u'294', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'6505556455', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'0', u'switch_id': u'', u'tz_dbid': u'PST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'Modem', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}, {u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'General', u'record_id': u'310', u'call_result': u'Unknown Call Result', u'daily_till': u'86340', u'group_id': u'', u'chain_id': u'295', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'6505559881', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'0', u'switch_id': u'', u'tz_dbid': u'PST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'Voice Mail', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}, {u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'General', u'record_id': u'311', u'call_result': u'Unknown Call Result', u'daily_till': u'86340', u'group_id': u'', u'chain_id': u'296', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'6505554872', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'0', u'switch_id': u'', u'tz_dbid': u'PST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'Pin Pager', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}]
#CallingListData = []
#CallingListData = cldata
#CallingListData = [{u'chain_n': u'0', u'record_status': u'Retrieved', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'General', u'record_id': u'167', u'call_result': u'Unknown Call Result', u'daily_till': u'86340', u'group_id': u'', u'chain_id': u'156', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'thompson@demosrv.genesyslab.com', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'0', u'switch_id': u'', u'tz_dbid': u'PST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'E-Mail Address', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}, {u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'General', u'record_id': u'168', u'call_result': u'Unknown Call Result', u'daily_till': u'86340', u'group_id': u'', u'chain_id': u'157', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'thompson@demosrv.genesyslab.com', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'0', u'switch_id': u'', u'tz_dbid': u'PST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'Instant Messaging', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}, {u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'General', u'record_id': u'169', u'call_result': u'Unknown Call Result', u'daily_till': u'86340', u'group_id': u'', u'chain_id': u'158', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'thompson@demosrv.genesyslab.com', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'43200', u'switch_id': u'', u'tz_dbid': u'PST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'[No Contact Type]', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}]
#CallingListData = [{u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'General', u'record_id': u'202', u'call_result': u'Unknown Call Result', u'daily_till': u'64800', u'group_id': u'', u'chain_id': u'187', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'6505556455', u'attempt': u'2', u'treatments': u'', u'call_time': u'', u'daily_from': u'28800', u'switch_id': u'', u'tz_dbid': u'IST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'Direct Business Phone', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}]
#CallingListData = {u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'General', u'record_id': u'72', u'call_result': u'Unknown Call Result', u'daily_till': u'86340', u'group_id': u'', u'chain_id': u'72', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'thompson@genesys.com', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'0', u'switch_id': u'', u'tz_dbid': u'PST', u'camp_name_0': u'Outbound contact - Sample Campaign', u'contact_info_type': u'E-Mail Address', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}
#print CallingListData[1]
#x=1
#block = ["Modem","VoiceMail","PinPager"]
#for x in range(3):
#CallListData = CallingListData[0]
#Qaart_Verification(CallListData)



#var=" "
#i=0
#for var in data:
#	try:
#		checcker = CallingListData.keys()[CallingListData.values().index(data[i])] 
#		print checcker
#	except ValueError:
#		checker=" "	
#	if checcker:
#		print "Passed"
#	i=i+1

x=0
block = ["AddRecord1","AddRecord2","AddRecord3","AddRecord4","AddRecord5"]
for x in range(5):
	CallListData = CallingListData[x]
	Qaart_Verification(CallListData,block[x])
	print block[x]