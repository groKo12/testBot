import os
from datetime import datetime
# General purpose function to write data to a file
def write_to_log(file_path, string, timestamp=datetime.now()):
    # strip file name off
    dir = os.path.dirname(file_path)
    print(dir)

    # Create dir if it doesn't exist
    os.makedirs(dir, exist_ok=True)

    with open(file_path, 'a') as f:
        f.write(timestamp + string)
    f.close()


