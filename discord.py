import requests, json, time, os
from gtts import gTTS

token = "Your Token XXXXXXXXXXXXXXXXXXXXXXXXX"

def send_message(channel_id, message):
    data = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", {"content":message}, headers={"authorization": token})
    return data.json()

def send_privet_message_name(user_name, message):
    data = requests.get('https://discord.com/api/v9/users/@me/channels', headers={"authorization": token}).json()
    for da in data:
        try:
            if (da['recipients'][0]['username'] == user_name):
                    channel_id= da['id']
                    send_message(channel_id, message)
        except:
            pass
        
def send_privet_message_id(user_id, message):
    data = requests.post("https://discord.com/api/v9/users/@me/channels", headers={"authorization": token,"content-type": "application/json"}, data=json.dumps({"recipient_id":user_id}))
    channel_id= data.json()['id']
    send_message(channel_id, message)

def edit_message(channel_id, message_id, message):
    data = requests.patch(f"https://discord.com/api/v7/channels/{channel_id}/messages/{message_id}", {"content":message}, headers={"authorization": token})
    return data.json()

#############################################################################
#its user_list every open chats you have the user_id = user-avatar, user-name
user_list = {}
data = requests.get('https://discord.com/api/v9/users/@me/channels', headers={"authorization": token}).json()
for da in data:
    try:
        user_list[da['id']] = [da['recipients'][0]['avatar'], da['recipients'][0]['username']]
    except:
        pass

def edit_channel(channel_id, name, icon=None):
    data = requests.patch(f"https://discord.com/api/v9/channels/{channel_id}", headers={"authorization": token,"content-type": "application/json"}, data=json.dumps({"name": f"{name}", "icon": f"{icon}"}))
    return data.json()

def delete_channel(channel_id):
    data = requests.delete(f'https://discord.com/api/v9/channels/{channel_id}', headers={"authorization": token})
    return data.json()

def add_user_group(channel_id, user_id):
    data = requests.put(f"https://discord.com/api/v9/channels/{channel_id}/recipients/{user_id}", headers={"authorization": token,"content-type": "application/json"}, data=json.dumps({"nick":"lolname"}))
    print(data.text) 

def remove_user_group(channel_id, user_id):
    data = requests.delete(f"https://discord.com/api/v9/channels/{channel_id}/recipients/{user_id}", headers={"authorization": token,"content-type": "application/json"}, data=json.dumps({"nick":"lolname"}))
    #its not give back json data/text
    
def create_group(name=None):
    data = requests.post("https://discord.com/api/v9/users/@me/channels", headers={"authorization": token,"content-type": "application/json"}, data=json.dumps({}))
    if (name == None):
        return data.json()
    return edit_channel(data.json()['id'], name)

def get_messages(channel_id):
    data = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers={"authorization": token})
    return data.json()
##############
#roles
def get_guild_roles(guild_id, role_id : int=None):
    data = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/roles', headers={"authorization": token})
    if role_id == None:
        return data.json()
    for role in data.json():
        if (int(role['id']) == role_id):
            return role
    #if not role in data its return the all data
    return data.json()

def delete_guild_role(guild_id, role_id):
    data = requests.delete(f'https://discord.com/api/v9/guilds/{guild_id}/roles/{role_id}', headers={"authorization": token})
    try:
        return data.json()
    except:
        return None
    
def create_guild_role(guild_id, name='new Roles_lol'):
    
    
    data = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/roles', data=(json.dumps({"name": name})), headers={"authorization": token,"content-type": "application/json"})
    return data.json()

def remove_guild_member(guild_id, user_id):
    data = requests.delete(f'https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}', headers={"authorization": token})
    return data.json()

"""
get_messages(channel_id, message_id)
edit_message(channel_id, message_id, content)
send_message(channel_id, content)
send_privet_message_id(User_id, content)
send_privet_message_name(User_name, content)
edit_channel(channel_id, name) # work on group
create_group(name)
add_user_group(channel_id, user_id)
remove_user_group(channel_id, user_id)
delete_channel(channel_id)
get_guild_roles(guild_id, role_id=None) # if you dont use role_id is give back the all roles data
create_guild_role(guild_id, name='new Roles_lol')
delete_guild_role(guild_id, role_id)
"""

##################################################
##################################################
##################################################
##################################################
#SOME TEST 
import requests
token = "Your Token XXXXXXXXXXXXXXXXXXXXXXXXX"

#event when you get message is print the message
messages_data = []
data = requests.get('https://discord.com/api/v9/users/@me/channels', headers={"authorization": token}).json()
for da in data:
    try:
        messages_data.append(da['last_message_id'])
    except:
        pass

last_channel = []

import threading
class runtask(object):
    def __init__(self, object, interval=1, ):
        self.interval = interval
        self.object = object

        thread= threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        time.sleep(4)
        last_channel.remove(self.object)


while True:
    data = requests.get("https://discord.com/api/v9/users/@me", headers={"authorization": token,"content-type": "application/json"})
    
    now_username = data.json()['username']
    data = requests.get('https://discord.com/api/v9/users/@me/channels', headers={"authorization": token}).json()
    
    for da in data:
        if (not da['last_message_id'] in messages_data):
            messages_data.append(da['last_message_id'])
            message_data = get_messages(da['id'])[0]
            if (str(now_username) == message_data["author"]["username"]):
                break
            print(f'New Message From {message_data["author"]["username"]} : {message_data["content"]}')
