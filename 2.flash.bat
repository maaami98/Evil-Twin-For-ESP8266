set COMPORT=COM3
python -m esptool --port %COMPORT% erase_flash
python -m esptool --port %COMPORT% --chip esp8266 write_flash 0x00000 "esp8266-20191220-v1.12.bin"
pause