@ECHO OFF

ECHO.:::::::::::::::::::::::::::::::::::::::::::::::::

ECHO.:: 					       ::

ECHO.::               BotChatContrast               ::

ECHO.:: 					       ::

ECHO.::               Author:   Null                ::

ECHO.:: 					       ::

ECHO.::               Version:  V1.0.4              ::

ECHO.:: 					       ::

ECHO.::               CreateTime: 2019.04.18        ::

ECHO.:: 					       ::

ECHO.:::::::::::::::::::::::::::::::::::::::::::::::::

ECHO.[ INFO ] Operational environment preparation

REM Install the environment dependent libraries from the configuration file
if exist requirements.txt pip install -r requirements.txt
if not exist requirements.txt echo requirements.txt does not exist

REM running script
python run.py
