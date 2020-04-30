from inotify_simple import INotify, flags
import subprocess
import os
import yaml
import glob
# import kubernetes
from kubernetes import client, config, utils

'''
version: v1
kind: DevConfig
data:
    script:
      - script 1
      - script 2
      - script 3
stages:
  - script
'''

general_config = {'version': 'v1', 'kind': 'DevConfig', 'data': {}, 'stages': []}

devignore = {}
# Note: Import the config first and then the client.
config.load_kube_config()
k8s_client = client.ApiClient()

def _dev_config_sh(files):    

    general_config['data']['scripts'] = files
    return general_config 

def _dev_config_k8s(files):

    general_config['data']['k8s'] = files
    return general_config

def _dev_config_create(context,files):

    if context == 'shell_script':
        return _dev_config_sh(files)
    elif context == "yaml_script":
        return _dev_config_k8s(files)

def _execute_config_file():

    config_data = _read_config()
    _execute_config_data(config_data)

def _read_config():

    with open('dev.yaml','r') as f:
        config_data = yaml.load(f, Loader=yaml.FullLoader)
    return config_data

def _execute_script(scripts):

    print('Execute script')
    for script in scripts:
        os.chmod(script,0o755)
        subprocess.call(script,shell=True)

def _execute_yaml(yaml_file):

    utils.create_from_yaml(k8s_client, yaml_file)

def _execute_yaml_script(yaml_scripts):

    for file in yaml_scripts['files']:
        _execute_yaml(file)

def _execute_stage(stage,config_file):

    print('execute stage')
    if stage == 'scripts':
        scripts = config_file['data']['scripts']
        _execute_script(scripts)
    elif stage == 'k8s':
        yaml_scripts = config_file['data']['k8s']
        _execute_yaml_script(yaml_scripts)

def _execute_config_data(config_file):

    stages = config_file['stages']
    for stage in stages:
        _execute_stage(stage,config_file)

    return None

def _check_devignore():
    print(list(yaml.load_all('.devignore.yaml',Loader=yaml.FullLoader)))
    

def dev_mode():

    directory = os.getcwd()
    inotify = INotify()
    _check_devignore()
    watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY | flags.DELETE_SELF
    inotify_object_list = []
    for (root,dirs,files) in os.walk(directory,topdown=True):
         inotify_object_list.append(inotify.add_watch(root, watch_flags))
    print('before loop')
    _execute_config_file()
    while True:
        event = inotify.read()
        print(event)
        if event:
            _execute_config_file()   

def init_mode():

    dir = os.getcwd()
    shell_script = glob.glob('./*.sh')
    yaml_script = glob.glob('./*.yaml')
    dockerfile_script = glob.glob('./Dockerfile')

    file_data = general_config
    shell_script.remove('./dev_notify.sh')
    yaml_script.remove('./dev.yaml')

    if shell_script:
        file_data = _dev_config_create('shell_script',shell_script)
        # print(file_data)
    if yaml_script:
        file_data = _dev_config_create('yaml_script',yaml_script)
        # print(file_data)

    with open('dev.yaml', 'w') as file:
        data = yaml.dump(file_data, file)


def main():
    print('Main function')

if __name__=='__main__':
    main()