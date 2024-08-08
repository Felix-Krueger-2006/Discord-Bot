import requests

async def is_valid_minecraft_username(username: str):
    api_url = f'https://api.mojang.com/users/profiles/minecraft/{username}'
    response = requests.get(api_url)

    if response.status_code == 200:
        return True
    else:
        return False
    
async def get_uuid_from_username(username: str):
    api_url = f'https://api.mojang.com/users/profiles/minecraft/{username.lower()}'
    response = requests.get(api_url)

    if response.status_code == 200:
        player_data = response.json()
        uuid = str(player_data['id'])
        uuid = '-'.join([uuid[:8], uuid[8:12], uuid[12:16], uuid[16:20], uuid[20:]])
        
        return uuid
    
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Fehler bei der Anfrage. Statuscode: {response.status_code}")

def get_minecraft_name(uuid):
    uuid = uuid.replace("-", "")
    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if data:
        current_name = data['name']
        return current_name
    else:
        return None

async def check_minecraft_player_amount(address):
    response = requests.get(f'https://api.mcsrvstat.us/2/{address}')
    data = response.json()

    if 'players' in data:
        return int(data['players']['online'])
    else:
        return None
    
async def check_minecraft_server(address):
    response = requests.get(f"https://api.mcsrvstat.us/2/{address}")
    data = response.json()
        
    if response.status_code == 200 and data.get('online'):
        return True
    else:
        return False