# Copyright (C) 2026 PeruvianWizard.
# All Rights Reserved.
# It may be used however you want as long as it doesn't break a law.

import _pickle

# Backs up dictionary with recent downloads into text file
def download_backup(dic):
    try:
        with open("media_urls.txt", "wb") as urls_save:
            _pickle.dump(dic, urls_save)
            print("BACKUP_CREATION_SUCCESS: Backup created successfully.")
    except Exception:
        print("BACKUP_CREATION_FAILURE: Backup could not be created.")

# Restore backup from text file
def restore_backup():
    dic = {}
    try:
        with open("media_urls.txt", "rb") as urls_open:
            dic = _pickle.load(urls_open)
            print("BACKUP_RESTORATION_SUCCESS: Backup restored successfully.")
            return dic
    except Exception:
        print("BACKUP_RESTORATION_FAILURE: There is no backup to restore.")
        return {}