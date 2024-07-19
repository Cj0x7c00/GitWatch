@echo off
set args=

:loop
if "%~1"=="" goto :end
set args=%args% %1
shift
goto :loop

:end
py .\GitWatch\gitwatch.py %args% 