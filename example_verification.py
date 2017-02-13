
class XML_Parse():

	def __init__(self, file_name, proj_base_path):

		self.file_name = file_name
		self.file_path = ""

		if not proj_base_path:
			SeriousError(1, "Project base path argument should not be blank")
		self.proj_base_path  = os.path.abspath(proj_base_path)
		if not os.path.exists(self.proj_base_path):
			SeriousError(1, "Project base path %s not exists on the system" % self.proj_base_path)
		if file_name:
			self.file_path = self.findFilePath()
		else:
			SeriousError(1, "file name argument should not be blank")

	def __str__(self):

		str_obj = "=========%s Object Instance Values===============\n" % self.__class__.__name__
		str_obj += "file name %s\n" % self.file_name
		str_obj += "file Path %s\n" % self.file_path
		str_obj += "Project Base Path%s\n" % str(self.proj_base_path)
		str_obj += "==============================================\n"
		return str_obj

	def getValueFromXML(self, find_tag, attr_name="", id_tag="", id_attr_name="", id_attr_val="",
						is_text=0, serious_error=1):

		if self.file_path:
			base_path = self.file_path
		elif serious_error:
			SeriousError(1, "File path is empty")
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
					SeriousError(1, "Error: Id tag is not found or attributes are invalid\n\id_tag %s \t id_attr_name %s \t id_attr_val %s" % (id_tag,id_attr_name,id_attr_val))
				else:
					return 0
			tag_list = tree.getElementsByTagName(find_tag)
			for tag in tag_list:
				if attr_name:
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
					SeriousError(1, "Error: %s tag or %s attribute is not found" % (find_tag,attr_name))
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
					SeriousError(1, "Error: %s tag or %s attribute is not found" % (find_tag,attr_name))
				else:
					return 0

# self.ipd_dig_parser.getValueFromXML("blocks","name",id_attr_name="xmi:type",id_attr_val="ipd:WorkflowBlock", serious_error=0)
	parser = XML_Parse(default.scxml,'C:\Python27\example')	
	str(parser);	