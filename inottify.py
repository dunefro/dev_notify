from inotify_simple import INotify, flags
import subprocess
import os
import yaml
import glob

'''
version: v1
kind: DevConfig
data:
    script:
      - script 1
      - script 2
      - script 3
'''
config = {'version': 'v1', 'kind': 'DevConfig', 'data': ''}

def _dev_config_sh(files):    
    config['data'] = {'script': files}
    return config 

def _dev_config_create(context,files):
    if context == 'shell_script':
        return _dev_config_sh(files)

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
    shell_script = glob.glob('./*.sh')
    yaml_script = glob.glob('./*.yaml')
    dockerfile_script = glob.glob('./Dockerfile')

    if shell_script:
        file_data = _dev_config_create('shell_script',shell_script)

    with open('dev.yaml', 'w') as file:
        data = yaml.dump(file_data, file)

def hello():
    print("hello this is amazing to see a function being called from the command line in python")

def main():
    print('Main function')

if __name__=='__main__':
    main()