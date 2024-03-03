import os, time

# General purpose function to write data to a file
def write_to_log(file_path, string, def_format="%Y-%m-%d %H:%M:%S"):
    # strip file name off
    dir = os.path.dirname(file_path)

    # Create dir if it doesn't exist
    os.makedirs(dir, exist_ok=True)

    # Grab Current time
    current_timestamp = time.time()
    formatted_time = time.strftime(def_format, time.gmtime(current_timestamp))


    # Write timestamped string to specified file
    with open(file_path, 'a') as f:
        time_string = formatted_time + " " + string
        f.write(time_string)
    f.close()


