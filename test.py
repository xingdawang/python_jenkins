import jenkins
import xml.etree.ElementTree as ET
import json
import time
import multiprocessing as mp
import Queue
import threading
output = mp.Queue()
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

def job_d(server, jobs):
	for job in jobs:
		each_job = server.get_job_info(job)
		# return each_job
		# print each_job['name']

def job_dd(job, server, output):
	# lock.acquire()
	each_job = server.get_job_info(job)
	output.put(each_job['name'])
	# print each_job['name']
	# return each_job
	# lock.release()







config = load_config();
server = connect_server(config['server_url'], config['username'], config['password'])
all_view_names = get_all_view_names(server)
# print all_view_names
jobs =  get_a_view_jobs(server, 'tab 1');



# start_time = time.time()
# job_d(server, jobs)
# print("--- %s seconds ---" % (time.time() - start_time))

# start_time = time.time()
# for job in jobs:
# 	Process(target=job_dd, args=(job, server)).start()

# print("--- %s seconds ---" % (time.time() - start_time))


processes = [mp.Process(target=job_dd, args=(job, server, output)) for job in jobs]

# Run processes
for p in processes:
    p.start()

# Exit the completed processes
for p in processes:
    p.join()

# Get process results from the output queue
results = [output.get() for p in processes]

print(results)