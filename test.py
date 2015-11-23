import jenkins
import xml.etree.ElementTree as ET

# Connect to server
#	return server: return the connect server information.
def connect_server():
	server = jenkins.Jenkins('http://localhost:8080', username='myuser', password='mypassword')
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







server = connect_server()
all_view_names = get_all_view_names(server)
print all_view_names
print get_a_view_jobs(server, 'tab 1');
job_info = server.get_job_config('iLife')

print job_info