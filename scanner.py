from scapy.all import *
import os, sys
import traceback
import urllib2 as urllib
BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

#The function returns your current working interface (wlan or wifi)
def getDefaultInterface(returnNet=False):
    def long2net(arg):
        if(arg <= 0 or arg >= 0xFFFFFFFF):
            raise ValueError("Illegal Netmask Value", hex(arg))
        return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))
    def to_CIDR_notation(bytes_network, bytes_netmask):
        network = scapy.utils.ltoa(bytes_network)
        netmask = long2net(bytes_netmask)
        net = "%s/%s" %(network, netmask)
        if netmask < 16:
            return None
        return net

    iface_routes = [route for route in scapy.config.conf.route.routes if route[3] == scapy.config.conf.iface and route[1] != 0xFFFFFFFF]
    network, netmask, _, interface, address = max(iface_routes, key=lambda item:item[1])
    net = to_CIDR_notation(network, netmask)
    if net:
        if returnNet:
            return net
        else:
            return interface

#This returns your MAC address,takes in the default interface name
def getDefaultInterfaceMAC(defaultInterface):
    try:
        defaultInterfaceMac = get_if_hwaddr(defaultInterface)
        if defaultInterfaceMac == "" or not defaultInterfaceMac:
            print("Error")
            defaultInterfaceMac = raw_input(header)
            return defaultInterfaceMac
        else:
            return defaultInterfaceMac
    except:
        print("Ex. Error")

#This returns your Gateway IP
#leave failSafe=true is you want the user to input the gateway in case of failure
def getGatewayIP(failSafe=True):
    try:
        getGateway_p = sr1(IP(dst="google.com", ttl=0) / ICMP() / "XXXXXXXXXXX", verbose=False)
        return getGateway_p.src
    except:
	if failSafe:
		# request gateway IP address (after failed detection by scapy)
		print("\n{0}ERROR: Gateway IP could not be obtained. Please enter IP manually.{1}\n").format(RED, END)
		header = ('{0}Scanner {1}> {2}Enter Gateway IP {3}(e.g. 192.168.1.1): '.format(BLUE, WHITE, RED, END))
		gatewayIP = raw_input(header)
        	return gatewayIP
	

#Uses API to fingerprint your device using MAC address
def resolveMac(mac):
    try:
        url = "https://macvendors.co/api/vendorname/"
        request = urllib.Request(url + mac, headers={'User-Agent': "API Browser"})
        response = urllib.urlopen(request)
        vendor = response.read()
        vendor = vendor.decode("utf-8")
        vendor = vendor[:25]
        return vendor
    except:
        return "N/A"

#Scans the network, in given interface, to generate list of live IPs
def scanNetwork(network):
    returnList = []
    import nmap
    nm = nmap.PortScanner()
    a = nm.scan(hosts=network, arguments='-sP')
    for k, v in a['scan'].iteritems():
        if str(v['status']['state']) == 'up':
            try:
                returnList.append([str(v['addresses']['ipv4']), str(v['addresses']['mac'])])
            except:
                pass

    return returnList

def getNodes():
    global nodelist
    nodelist=[]
    try:
        nodelist = scanNetwork(getDefaultInterface(True))
    except KeyboardInterrupt:
        printf("Terminated.")
    except:
        print("Error.")
    generateIPs()
    return nodelist

#Create list of IPs that were found live
def generateIPs():
    global liveIPs
    liveIPs = []
    for host in nodelist:
        liveIPs.append(host[0])
    return liveIPs


if __name__=='__main__':
	print("Running")
	defaultInterface = getDefaultInterface()
	defaultGatewayIP = getGatewayIP()
	defaultInterfaceMac = getDefaultInterfaceMAC(defaultInterface)
	print("Network Details: ")
	print("Default Network Interface: " + defaultInterface)
	print("Your Gateway IP: " + defaultGatewayIP)
	print("Your MAC Address: " + defaultInterfaceMac)
	getNodes()
	print(nodelist) #This list contains both IP and MAC addresses
	print("IP thinggy")
	print(liveIPs) #This list only contains their IP addresses

	print("Real Thinggy")
	for i in range(len(liveIPs)):
	    mac = ""
	    for host in nodelist:
		if host[0] == liveIPs[i]:
		    mac = host[1]
	    vendor = resolveMac(mac)
	    #print(mac)
	    print("  [{0}" + str(i) + "{1}] {2}" + str(liveIPs[i]) + "{3}\t" + mac + "{4}\t" + vendor + "{5}").format(YELLOW, WHITE, RED, BLUE, GREEN, END)
