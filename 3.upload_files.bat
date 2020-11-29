set COMPORT=COM3

ampy --port %COMPORT% --baud 115200 put server.py
ampy --port %COMPORT% --baud 115200 put captive_http.py
ampy --port %COMPORT% --baud 115200 put captive_dns.py
ampy --port %COMPORT% --baud 115200 put main.py
ampy --port %COMPORT% --baud 115200 put sample.html
ampy --port %COMPORT% --baud 115200 put tplink.main.css
ampy --port %COMPORT% --baud 115200 put tplink.html
ampy --port %COMPORT% --baud 115200 put tplink.favicon.ico

pause
