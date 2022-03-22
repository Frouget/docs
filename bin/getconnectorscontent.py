# to do:
# Add API request parameter to for single connector 
# Add flags to restrict to md or json
# Add flag to overwrite existing md and json or write new files only
# Add temp section to append placeholder json until fields added and populated in the connectors db/API response
# Confirm naming conventions
# Confirm permalinks
# windows cli : python getconnectorscontent.py

import requests
import re
import os
import json

response = requests.get('https://my.cyclr.com/api/connectors?pageSize=1000&details=true')
if response.status_code == 200 :
	json_data = response.json()

	template_md = os.path.join(os.path.dirname(__file__), './assets/template.md')
	# print(__file__)
	# print(template_md)
	# parse each connector in the response array
	for item in json_data:
		# derive the connector filenames 
		connector_name = item['Name']
		connector_icon = item['Icon']
		connector_description = item['Description']
		connector_category = 'All'
		connector_categories = ",".join(item['Categories'])
		file_name = re.sub("[^a-zA-Z0-9]", "", connector_name).lower()
		file_md = '../pages/connectors-new/connector-'+file_name+'.md'
		file_md_full = os.path.join(os.path.dirname(__file__), file_md)
		file_json = "../_data/connectors-new/connector-"+file_name+".json"
		file_json_full = os.path.join(os.path.dirname(__file__), file_json)
		# print("Write md "+file_md_full+" and json "+file_json_full)
		if type(item['Categories']) is list and item['Categories']:
			connector_category = item['Categories'][0]
		# inject the connector name into the md template
		# open the template file and the new file
		with open(template_md,'r') as fromfile, open(file_md_full,'a') as tofile:
			for line in fromfile:
				# omit description from front matter if no value
				if "connectordescription" in line and connector_description is None:
					continue					
				elif "connectordescription" in line:
					newline = re.sub("connectordescription", connector_description, line)
				elif "connectortitle" in line:
					newline = re.sub("connectortitle", connector_name, line)
				elif "connectoricon" in line:
					newline = re.sub("connectoricon", connector_icon, line)
				elif "connectorcategory" in line:
					newline = re.sub("connectorcategory", connector_category, line)
				elif "connectorcategories" in line:
					newline = re.sub("connectorcategories", "["+connector_categories+"]", line)
				elif "connectorname" in line:
					newline = re.sub("connectorname", file_name, line)
				else:
					newline = line
				# append to new md
				tofile.write(newline)

		# write the connector object to the json file
		json_string = json.dumps(item, indent=4)
		with open(file_json_full, "w") as filejson:
			filejson.write(json_string)