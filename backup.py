import os
import shutil
import time
import json

import os
import shutil
import time
import json

class FileBackup:
    def __init__(self, settings_file):
        with open(settings_file) as f:
            settings = json.load(f)

        self.database_folder = settings['database_folder']
        self.database_backup_folder = settings['database_backup_folder']
        self.database_file_name = settings['database_file_name']
        self.database_file_extension = settings['database_file_extension']
        self.database_full_path = os.path.join(self.database_folder, self.database_file_name + '.' + self.database_file_extension)

        # Get the initial file size and modification time
        self.initial_file_size = os.path.getsize(self.database_full_path)
        self.initial_modification_time = os.path.getmtime(self.database_full_path)

        self.backup_timeing = settings['backup_timeing']

    def run(self):
        while True:
            # Wait for the specified time
            time.sleep(self.backup_timeing)

            # Check if the file size or modification time has changed
            current_file_size = os.path.getsize(self.database_full_path)
            current_modification_time = os.path.getmtime(self.database_full_path)

            if current_file_size != self.initial_file_size or current_modification_time != self.initial_modification_time:
                # If the file has changed, create a new backup with a unique name
                backup_time = time.strftime("%Y-%m-%d_%H-%M-%S")
                backup_file_name = os.path.join(self.database_backup_folder, self.database_file_name + '_' + backup_time + '.' + self.database_file_extension)
                print('Backing up file {} to {}'.format(self.database_full_path, backup_file_name))
                shutil.copy2(self.database_full_path, backup_file_name)

                # Update the initial file size and modification time
                self.initial_file_size = current_file_size
                self.initial_modification_time = current_modification_time