@echo off    
start cmd /k "cd /d %~dp0&&pyinstaller 1_complex.spec"

