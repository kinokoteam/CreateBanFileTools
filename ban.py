import requests
import json
from datetime import datetime

def get_uuid(mcid):
    response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{mcid}')
    if response.status_code == 200:
        return response.json()['id']
    else:
        return None

def create_ban_entry(uuid, mcid):
    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")
    ban_entry = [{
        "uuid": uuid,
        "name": mcid,
        "created": created_time,
        "source": "Server",
        "expires": "forever",
        "reason": "Python Auto Ban Tool"
    }]
    return ban_entry

def write_to_file(ban_entry):
    with open('banned-players.json', 'w') as file:
        json.dump(ban_entry, file, indent=2)

def main():
    with open('ban.txt', 'r') as f:
        mcids = f.read().splitlines()

    ban_entries = []
    for mcid in mcids:
        uuid = get_uuid(mcid)
        if uuid:
            ban_entry = create_ban_entry(uuid, mcid)
            ban_entries.extend(ban_entry)

    write_to_file(ban_entries)

if __name__ == "__main__":
    main()
