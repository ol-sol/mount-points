import json, shutil
from datetime import datetime
from time import strftime
import read_fstab as rfs

rfs.fstab_to_json()

class Mounting:
    def __init__(self):
        with open('host_mounts/host_mounts.json', 'r') as j:
            self.mounts = json.load(j)

    def save(self, lst):
        shutil.copy('host_mounts/host_mounts.json', f"backups/host_mounts_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json")
        to_json= json.dumps(lst)
        with open('host_mounts/host_mounts.json', 'w') as file:
            file.write(to_json)
        for server in lst:
            with open(f"host_scripts/{server['server']}.sh", "w") as file:
                for row in server["mount_points"]:
                    file.writelines(row["row"]+"\n")
                
        

    def sync(self):
        print('Synced')
