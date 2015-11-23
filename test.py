import jenkins
import xml.etree.ElementTree as ET
import json

# Load config from json file
#	return json format config
def load_config():
	with open("config.json") as json_file:
	    json_data = json.load(json_file)
	return json_data

# Connect to server
#	param server_url: the url of the server, if port is specified, use the format as '8.8.8.8:8080'
#	param username: the name of the user
#	param password: the password of the user
#	return server: return the connect server information.
def connect_server(server_url, username, password):
	server = jenkins.Jenkins(server_url, username, password)
	return server


# Get all views' names
#	param connected_server: get connected server information
#	return all_view_names: return all of the views' name
def get_all_view_names(connected_server):
	#x = connect_server()
	all_view_names = []
	all_views = connected_server.get_views()
	for each_view in all_views:
		all_view_names.append(each_view['name'])
	return all_view_names

# Get a view all jobs
#	param connected_server: get connected server information
#	param view_name: the name attribute of a view
#	return all jobs under the given view_name
def get_a_view_jobs(connected_server, view_name):
	xml = connected_server.get_view_config(view_name)
	tree = ET.fromstring(xml)
	all_jobs = []
	for job_name in tree.findall('jobNames'):
		# recursively find the child
		for each_name in job_name:
			if each_name.text is not None:
				all_jobs.append(each_name.text)
	return all_jobs






config = load_config();
server = connect_server(config['server_url'], config['username'], config['password'])
all_view_names = get_all_view_names(server)
print all_view_names
print get_a_view_jobs(server, 'tab 1');
#job_info = server.get_job_config('iLife')

#print job_info
