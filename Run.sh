#!/bin/bash
echo OFF

echo .:::::::::::::::::::::::::::::::::::::::::::::::::

echo .::

echo .::               BotChatContrast

echo .::

echo .::               Author:   Null

echo .::

echo .::               Version:  V1.0.4

echo .::

echo .::               CreateTime: 2019.04.18

echo .::

echo .:::::::::::::::::::::::::::::::::::::::::::::::::

echo .[ INFO ] Operational environment preparation

# REM Install the environment dependent libraries from the configuration file
if [ -f requirements.txt ];
then
     pip install -r requirements.txt
fi
if [ ! -f requirements.txt ];
then
    echo requirements.txt does not exist
fi

echo .[INFO] running script
python3 run.py