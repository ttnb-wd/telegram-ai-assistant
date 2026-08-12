import shutil
import os
from datetime import datetime


SOURCE = "memory.db"
BACKUP_FOLDER = "backups"


def create_backup():

    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)


    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    backup_file = f"{BACKUP_FOLDER}/memory_{timestamp}.db"


    shutil.copy(
        SOURCE,
        backup_file
    )


    print("Backup created:")
    print(backup_file)



if __name__ == "__main__":

    create_backup()