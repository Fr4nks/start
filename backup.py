
# Code has been written specifically for windows 10.
# CHECK THIS OUT!
# https://ib-aid.com/en/optimized-firebird-configuration/

from datetime import datetime, timedelta
import socket
import struct
import os
import shutil
import time
import json
import subprocess

def RequestTimefromNtp(addr='0.de.pool.ntp.org'):
    REF_TIME_1970 = 2208988800  # Reference time
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    try: 
        client.sendto(data, (addr, 123))
        data, address = client.recvfrom(1024)
        t = struct.unpack('!12I', data)[10]
        t -= REF_TIME_1970
        dt = datetime.utcfromtimestamp(t)
        print(dt, 'NTP server time')
        return dt
    except:
        #if NTP time is not available, backup to a different folder. 
        try:
            print('Warning, if this program does not have admistrative priv')
            output = subprocess.check_output("w32tm /query /configuration")
            output_str = output.decode("utf-8")
            "AnnounceFlags" in output_str and "5" in output_str.split("AnnounceFlags")[1]
            dt = datetime.utcnow()
            print('Warning, no connection, using UTC time')
            print(dt, "Windows time setting is set to 'auto'")
            return dt
        except:
            print("Warning! Windows time setting is not set to auto. Backup have been turned off.")
            return None
    
class FileBackup:
    def __init__(self, settings_file):
        with open(settings_file) as f:
            settings = json.load(f)

        self.database_folder = settings['database_folder']
        self.database_file_name = settings['database_file_name']

        self.database_backup_folder = settings['database_backup_folder']
        
        self.database_file_extension = settings['database_file_extension']
        self.database_full_path = os.path.join(self.database_folder, self.database_file_name + '.' + self.database_file_extension)

        # Get the initial file size and modification time
        self.initial_file_size = os.path.getmtime(self.database_full_path)
        
        
        self.backup_interval = settings['backup_interval']

        self.hourly_backup_folder = os.path.join(self.database_backup_folder, 'hourly')
        self.daily_backup_folder = os.path.join(self.database_backup_folder, 'daily')
        self.monthly_backup_folder = os.path.join(self.database_backup_folder, 'monthly')

        print(self.database_full_path)

    def run(self):
        while True:
            # Wait for the specified time
            
            time.sleep(self.backup_interval)
            # Check if the file size or modification time has changed
            current_file_size = os.path.getmtime(self.database_full_path)
            print(current_file_size == self.initial_file_size, current_file_size, self.initial_file_size)
            self.initial_modification_time = RequestTimefromNtp()
            # Convert FILETIME to Python datetime object
            if current_file_size != self.initial_file_size and self.initial_modification_time != None:
                # If the file has changed, create a new backup with a unique name
                self.initial_file_size = current_file_size
                backup_time = self.initial_modification_time.strftime("%Y-%m-%d_%H-%M-%S")
                backup_file_name = os.path.join(self.hourly_backup_folder, self.database_file_name + '_' + backup_time + '.' + self.database_file_extension)
                daily_backup_file_name = os.path.join(self.daily_backup_folder, self.database_file_name + '_' + backup_time + '.' + self.database_file_extension)
                monthly_backup_file_name = os.path.join(self.monthly_backup_folder, self.database_file_name + '_' + backup_time + '.' + self.database_file_extension)
                
                print('Backing up file {} to {}'.format(self.database_full_path, backup_file_name))
                shutil.copy2(self.database_full_path, backup_file_name)

                backup_files = os.listdir(self.hourly_backup_folder)
                backup_files.sort(key=lambda f: os.path.getmtime(os.path.join(self.hourly_backup_folder, f)), reverse=True)
                for file_name in backup_files[6:]:
                    os.remove(os.path.join(self.hourly_backup_folder, file_name))
                
                daily_backup_files = os.listdir(self.daily_backup_folder)
                daily_backup_files.sort(key=lambda f: os.path.getmtime(os.path.join(self.daily_backup_folder, f)), reverse=True)
                
                #con = fdb.connect(dsn=backup_file_name, user='sysdba', password='masterkey')
                #cur = con.cursor()
                #cur.execute('SET TRANSACTION READ WRITE')
                #cur.execute('SWEEP TABLE CONTRACT')
                #con.commit()
                #cur.close()
                #con.close()

                for i, file_name in enumerate(daily_backup_files):
                    file_date = datetime.strptime(file_name[len(self.database_file_name)+1:-4], '%Y-%m-%d_%H-%M-%S')
                    if file_date.date().day == self.initial_modification_time.day:
                        os.remove(os.path.join(self.daily_backup_folder, file_name))
                    elif i >= 7:
                        os.remove(os.path.join(self.daily_backup_folder, file_name))

                shutil.copy2(self.database_full_path, daily_backup_file_name)

                monthly_backup_files = os.listdir(self.monthly_backup_folder)
                monthly_backup_files.sort(key=lambda f: os.path.getmtime(os.path.join(self.monthly_backup_folder, f)), reverse=True)

                for i, file_name in enumerate(monthly_backup_files):
                    file_date = datetime.strptime(file_name[len(self.database_file_name)+1:-4], '%Y-%m-%d_%H-%M-%S')
                    if file_date.date().month == self.initial_modification_time.month:
                        os.remove(os.path.join(self.monthly_backup_folder, file_name))
                    elif i >= 12:
                        os.remove(os.path.join(self.monthly_backup_folder, file_name))

                shutil.copy2(self.database_full_path, monthly_backup_file_name)

