from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import time

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

def uploadFile(file):
    gfile = drive.CreateFile({'parents': [{'id': '1SSUIKtlUZENTS59yIR7TDMGh_pR4OGM0'}]})
    # Read file and set it as the content of this instance.
    gfile.SetContentFile(file)
    gfile.Upload()  # Upload the file

print("videoUploader.py is ready!")

while True:
    is_file_uploaded = False
    try:
        for file in os.listdir("."):
            if file.endswith(".avi") and not file == "output.avi":
                uploadFile(file)
                print("Uploaded file " + file)
                os.remove(file)
                print("Removed file" + file)
                is_file_uploaded = True
    except:
        pass
    if not is_file_uploaded:
        time.sleep(5)
