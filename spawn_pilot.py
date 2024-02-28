import os
import shutil
import zipfile
import time
from datetime import datetime, timedelta
import json
import logging
import argparse
import math

def startup():
    file_name = "spawn_pilot_config.json"
    try:
        # Reading data from the JSON file
        with open(file_name, 'r') as json_file:
            loaded_data_list = json.load(json_file)
        print("Starting program...")
    except:
        first_startup(True)
        logging.warning("Config file restored, exiting!")
        exit()

    check = loaded_data_list["first_launch"]
    max_backups = loaded_data_list["max_backups"]
    regions_to_save = loaded_data_list["regions_to_save"]
    path_to_regions = loaded_data_list["path_to_regions"]
    backup_timer_seconds = loaded_data_list["backup_timer_seconds"]
    return check, max_backups, regions_to_save, path_to_regions, backup_timer_seconds



def main():
    parser = argparse.ArgumentParser(description='Spawn Pilot')

    # Add arguments
    parser.add_argument('-version', action='store_true', help='Show program version')
    parser.add_argument('-start', action='store_true', help='Start program')
    parser.add_argument('-calc', action='store_true', help='Start program')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Check the values of arguments and perform actions accordingly
    if args.version:
        print('Spawn Pilot 1.0')
    elif args.start:
        spawn_pilot(source_folder, "backup", max_backups, regions_to_save, timer)
    elif args.calc:
        region_calc()
    else:
        print('No valid option provided. Use -h or --help for help.')



def first_startup(check):
    if check:
        data = {
            "max_backups": 6,
            "regions_to_save": ["r.0.0.mcr", "r.-1.0.mcr", "r.-1.-1.mcr", "r.0.-1.mcr"],
            "path_to_regions": "lunatech/dimensions/0/region",
            "backup_timer_seconds": 1800,
            "first_launch": False,
        }

        file_name = "spawn_pilot_config.json"

        with open(file_name, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Config file created {file_name}")


def spawn_pilot(source_folder, destination_folder, max_backups, regions, timer):
    print("Program started!")
    def backup_files(source_folder, destination_folder, max_backups):
        # Ensure source and destination folders exist
        os.makedirs("backup", exist_ok=True)
        if not os.path.exists(source_folder) or not os.path.exists(destination_folder):
            print("Source or destination folder does not exist.")
            return

        # Get current time for zip file name
        current_time = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        zip_filename = f"backup_{current_time}.zip"

        # Get list of files to copy
        files_to_copy = regions  # Adjust file names accordingly

        # Copy files to destination folder
        for file_name in files_to_copy:
            source_path = os.path.join(source_folder, file_name)
            destination_path = os.path.join(destination_folder, file_name)
            shutil.copy(source_path, destination_path)

        # Zip the copied files
        with zipfile.ZipFile(os.path.join(destination_folder, zip_filename), 'w') as zip_file:
            for file_name in files_to_copy:
                file_path = os.path.join(destination_folder, file_name)
                zip_file.write(file_path, os.path.basename(file_path))

        # Remove oldest backup if exceeding the limit
        existing_backups = sorted([f for f in os.listdir(destination_folder) if f.startswith("backup_")], reverse=True)
        if len(existing_backups) > max_backups:
            oldest_backup = existing_backups[-1]
            os.remove(os.path.join(destination_folder, oldest_backup))
            print(f"Removed oldest backup: {oldest_backup}")

    while True:
        backup_files(source_folder, destination_folder, max_backups)
        print("Backup completed at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(timer)  # Sleep for 30 minutes


def region_calc():
    x, z = input("Please input two coordinates seperated by a space: ").split()
    try:
        x, z = int(x), int(z)
        region_xz = lambda x, z: (math.floor(x / 32), math.floor(z / 32))
        temp = region_xz(x, z)
        print(f"The region file will be called: r.{temp[0]}.{temp[1]}.mcr")
    except:
        print("failure, try again, maybe don't input letters or symbols that aren't numbers")
    exit()

if __name__ == "__main__":
    temp = startup()

    regions_to_save = temp[2]
    source_folder = temp[3]
    destination_folder = "backup"
    max_backups = temp[1]
    timer = temp[4]

    main()
