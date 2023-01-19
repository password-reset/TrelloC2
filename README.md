# TrelloC2
Simple C2 over Trello's API (Proof-of-Concept)

By: Fabrizio Siciliano

![screenshot](https://raw.githubusercontent.com/securemode/TrelloC2/master/screenshot.png)

### Update 12/30/2019
Removed hardcoded API key and Token, use input() instead.

### Requirements
Python 3.x

### Setup
1. Create a Trello account: https://trello.com/signup
2. Once logged in, get your API key: https://trello.com/app-key
3. Generate a Token (same page as app-key, follow the "Token" link)
4. Save both API key and Token, they're used in both the agent and operator scripts.
5. Browse to your board https://trello.com/b/[random]/[membername].json to get the list ID which is required in the agent script. You can find this in the json output under the "lists" item and within the "Things To Do" item "id" value.

### Usage
1. Run agent.py on the target system. This is the implant, and once run, will supply the operator with a "CID" value. This is the card ID and is needed on the operator-side.
2. Run the operator.py script on the attacker host. It will prompt for the agent's CID which is provided at agent.py runtime.
3. Do what thou wilt...
4. The operator script currently only has two commands; "show_commands" and "kill_implant". The "show_commands" command simply prints the help menu while the "kill_implant" command deletes the card associated with agent which terminates the agent connection. Typing "?" at the operator prompt will also display the commands menu.

### Limitations
- The Trello API "description" field for cards, which is used for temporarily storing commands and resulting command output, is limited in size. I think it's something around 16k characters. This is OK for most commands, however, commands that return large output will cause the agent to die due to the Trello API returning a 400 Bad Request (size too large) status. Be mindful of commands and their expected outputs. I'll eventually work in some logic to determine command output size before sending it back to trello's servers for operator consumption.

- This is not OPSEC-safe. All commands and command output will temporarily pass through Trello's servers and output will exist in the agents' "card" in cleartext temporarily. Although the traffic is TLS encrypted (in-transit) courtesy of Trello, and although the operator script makes an effort to "wipe the slate" clear of the command output, there's no telling whether this information is stored indefinitely. Ideally, the commands and command output should be saved to a "card" in an encrypted format, (i.e., AES), pulled down, and decrypted locally. This hasn't been built into the tool yet, and in its current state would require the machine the agent lives on to have certain libraries which might not be present in a default situtation. (Something to work on)

- The operator script and implant are currently both designed to be run on Linux-based boxes. Windows implants are a work in progress at this point in time.

### Misc
Note: This is simply a proof-of-concept to demonstrate legitimate services as command and control infrastructure and is 100% in alpha dev. Use at your own risk and on systems you've been authorized to access. (i.e., wherever the agent lives)

### Credits (ideas and concepts inspired by other works): 
- https://github.com/daniel-infosec/wikipedia-c2
- https://github.com/PaulSec/twittor 
- https://github.com/Coalfire-Research/Slackor
 

