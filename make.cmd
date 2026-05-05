@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\make.ps1" %*
exit /b %ERRORLEVEL%
