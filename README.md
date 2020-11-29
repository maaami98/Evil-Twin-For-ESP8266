# Evil-Twin-For-ESP8266
Evil Twin Attack For ESP8266, Captive Portal + Fake AP + Changeable Index, Micropython

## Installation
run 1.install_module.bat

Change the com port number written in 2.flash.bat and run 
end reset esp8266

Change the com port number written in 3.upload_files.bat and run


4.connect_serial.bat run and test!

## Upload other index
Examine sample.html 
```
cp sample.html sample2.html
```
edit sample2.html
```
ampy --port %COMPORT% --baud 115200 put sample2.html
```

## Test
```
python -m serial.tools.miniterm %COMPORT% 115200
```
