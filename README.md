# dev_notify
Application tool for deployment of your application in a fast manner. This will help in rolling changes instantly and only for development phase of any app.

Look at the dev.yaml file and realise how to mention the files that you want to re-deploy.

There are , as of now , two types of files that you can mention to work this tool out for you.
These are kubernetes custom object file specified in yaml specification and bash scripts. It is customized to work for linux OS only.


For all the directories that you want to not include in the dev setup you can mention their names in the .devignore.yaml in the following format
```
directories:
  - type: directory 
    path: <directory name that we wish to not include>
    # removes the entire directory from the scanning process
  - type: directory
    path: dir_name  # with respect to the current context
    except:
      - <list of file name that you still want to count for scanning relative to changes>
  - type: file
    path: <file name path that we wish to not include for scanning>
```
