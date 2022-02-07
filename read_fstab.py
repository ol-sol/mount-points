import pandas as pd
import glob, json
from pathlib import Path

def fstab_to_json():
    my_file = Path('host_mounts/host_mounts.json')
    if not my_file.is_file():
        file_names = glob.glob("host_mounts/*.zfs_fstab")
        mounts = [{"server": 
                        Path(file).stem, 
                "mount_points": 
                        [{"mp": row[1], "row": "sudo mount -t " + row[2] + " -o " + row[3]+ " " + row[0] + " " + row[1]} for row in pd.read_csv(file, delimiter=' ', header=None).to_numpy().tolist()]
                        } for file in file_names]

        to_json= json.dumps(mounts)

        with open(my_file, 'w') as file:
                file.write(to_json)

