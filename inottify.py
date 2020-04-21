from inotify_simple import INotify, flags
import subprocess
import os

inotify = INotify()
watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY | flags.DELETE_SELF
wd = inotify.add_watch('/home/ubuntu/workspace/new', watch_flags)
file_name = '/home/ubuntu/workspace/new/deploy.sh'
print('before loop')
while True:
    event = inotify.read()
    if event:
        print(event)
        print('calling the script')
        os.chmod(file_name,0o755)
        subprocess.call(file_name,shell=True)
