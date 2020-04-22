#!/bin/bash

if [[ $1 == 'init' ]]
then
    dir='$(echo $PWD)'
    # echo $dir
    python3 -c 'import inottify as dev; dev.init_mode()'
elif [[ $1 == 'dev' ]]
then
    python3 -c 'import inottify as dev; dev.dev_mode()'
else
    echo 'Enter the launch mode'
fi
