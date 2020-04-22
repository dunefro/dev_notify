from inotify_simple import INotify, flags
import subprocess
import os
import yaml
import glob


def dev_mode():
    directory = os.getcwd()
    inotify = INotify()
    watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY | flags.DELETE_SELF
    wd = inotify.add_watch(directory, watch_flags)
    file_name = '/home/ubuntu/workspace/new/deploy.sh'
    print('before loop')
    while True:
        event = inotify.read()
        if event:
            print(event)
            print('calling the script')
            os.chmod(file_name,0o755)
            subprocess.call(file_name,shell=True)    

def init_mode():
    dir = os.getcwd()
    print(glob.glob('./*.sh'))
    # print(dir)

def hello():
    print("hello this is amazing to see a function being called from the command line in python")