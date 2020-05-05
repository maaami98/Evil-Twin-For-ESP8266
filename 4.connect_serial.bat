@echo off
set COMPORT=COM3
echo Press Reset Button
python -m serial.tools.miniterm %COMPORT% 115200