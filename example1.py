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























def Qaart_Verification_Multi_blocks1(CallingListData,id_attr_val1,proj_base_path):
#	print CallingListData
	parser = XML_Parser("default12.scxml",proj_base_path) 
	script_data =  parser.getValueFromXML("script",is_text=1,id_tag="state",id_attr_name="id",id_attr_val=id_attr_val1, serious_error=0)
	print(script_data)
	pattern = '''\w+\[\'\w+\'\]\[\'(.*)\'\]\s*=\s*\'*(.*?)\'*;'''
	key =[]
	data = []
	data_n = {}
	it = re.finditer(pattern,script_data)
	for match in it:
		data.append(match.group(2))
		key.append(match.group(1))
		data_n[match.group(1)]=match.group(2)
	print(data)
	print(key)
	print( data_n)
	dic = {}
	i=0
	#l=0
	#k = get_Var_Value(data[7],parser)
	#print data[7]
	#data[7] = k
	#data_n[key[7]] = k
	record_type_dic = {'Personal Rescheduled ':'4','Personal Callback':'5','Campaign Callback':'6','No Call':'7','General':'2','Unknown':'1','Campaign Rescheduled':'3'}
	for l in range(len(data)):
		try:
			chkr = record_type_dic.keys()[record_type_dic.values().index(data[l])]
			print chkr
			if chkr:
				data[l]= chkr
				data_n[key[l]]= chkr
		except ValueError:
			chkr=" "
	print(data)
	for var in data:
		try:
			chk = CallingListData.keys()[CallingListData.values().index(data[i])]	
			dic[key[i]]=chk;

		except ValueError:
			chk=" "	
		i=i+1
	print(dic)
	dic_f = {}
	for key,value in dic.iteritems():
		dic_f [value] = data_n[key]
	print(dic_f)

	for key,value in dic_f.iteritems():
		if dic_f [key] == CallingListData[key]:
			print("Passed") 
		else:
			SeriousError( "failed - Wrong Value update in database")
			












CallingListData =[{u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'Personal Rescheduled', u'record_id': u'2082', u'call_result': u'Unknown Call Result', u'daily_till': u'86340', u'group_id': u'', u'chain_id': u'2024', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'6505556455', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'0', u'switch_id': u'', u'tz_dbid': u'IST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'Direct Business Phone', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}, {u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'Personal CallBack', u'record_id': u'2083', u'call_result': u'Unknown Call Result', u'daily_till': u'86340', u'group_id': u'', u'chain_id': u'2025', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'6505556455', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'0', u'switch_id': u'', u'tz_dbid': u'IST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'Direct Business Phone', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}, {u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'Campaign CallBack', u'record_id': u'2084', u'call_result': u'Unknown Call Result', u'daily_till': u'86340', u'group_id': u'', u'chain_id': u'2026', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'6505556455', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'0', u'switch_id': u'', u'tz_dbid': u'IST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'Direct Business Phone', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}, {u'chain_n': u'0', u'record_status': u'Ready', u'media_ref': u'', u'dial_sched_time': u'', u'record_type': u'No Call', u'record_id': u'2085', u'call_result': u'Unknown Call Result', u'daily_till': u'86340', u'group_id': u'', u'chain_id': u'2027', u'email_template_id': u'', u'agent_id': u'', u'contact_info': u'6505556455', u'attempt': u'0', u'treatments': u'', u'call_time': u'', u'daily_from': u'0', u'switch_id': u'', u'tz_dbid': u'IST', u'camp_name_0': u'Outbound Contact - Sample Campaign', u'contact_info_type': u'Direct Business Phone', u'app_id': u'', u'email_subject': u'', u'campaign_id': u'107'}]
x=0
block = ["AddRecord1","AddRecord2","AddRecord3","AddRecord4"]
for x in range(4):
	CallListData = CallingListData[x]

	print (block[x])
	Qaart_Verification_Multi_blocks1(CallListData,block[x],"C:\Python27\example")
