@echo off
set projectName=
set fileName=
set filePath=
goto main
:main
set d=%date:~0,10%
set t=%time:~0,8%
set /p "filePath=File Path:"
set /p "projectName=Project Name:"
set /p "fileName=File Name:"
if defined projectName (goto name) else goto nullName
:nullName
set "forders=%filePath:\= %"
for %%a in (%forders%) do set projectName=%%a
goto name
:name
for %%i in (%fileName%) do (set file_type=%%~xi)
if "%file_type%"==".c" (goto cpp) else if "%file_type%"==".py" (goto python) else (goto default)
:cpp
set line0=/*==================================================
set line1=*	Project Name: %projectName%
set line2=*	File Name	: %fileName%
set line3=*	Author		: HuangDaTian
set line4=*	Create Time	: %d% %t%
set line5=*	Modify Time	: %d% %t%
set line6=*	Description	: 
set line7=*==================================================*/
set line8=#include ^^^<iostream^^^>
goto istream
:python
set line0=# -*- coding: utf-8 -*-
set line1=#==================================================
set line2=#	Project Name: %projectName%
set line3=#	File Name	: %fileName%
set line4=#	Author		: HuangDaTian
set line5=#	Create Time	: %d% %t%
set line6=#	Modify Time	: %d% %t%
set line7=#	Description	: 
set line8=#==================================================*/
goto istream
:default
pause
:end
pause
:istream
if defined filePath (goto next) else goto end
:next
@echo %line0%>>%filePath%\%fileName%
@echo %line1%>>%filePath%\%fileName%
@echo %line2%>>%filePath%\%fileName%
@echo %line3%>>%filePath%\%fileName%
@echo %line4%>>%filePath%\%fileName%
@echo %line5%>>%filePath%\%fileName%
@echo %line6%>>%filePath%\%fileName%
@echo %line7%>>%filePath%\%fileName%
@echo %line8%>>%filePath%\%fileName%
