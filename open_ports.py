#To use this function ,use following commands in scanner.py
#import open_ports
#open_ports.openPorts()

import scanner
YELLOW = scanner.YELLOW
RED = scanner.RED
END = scanner.END
BLUE = scanner.BLUE
WHITE = scanner.WHITE
def openPorts() :
	scanner.getNodes()
	import nmap
	nm = nmap.PortScanner()
	for host in scanner.nodelist :
		try:
			a = nm.scan(hosts=host[0])
			b = nm[host[0]].all_tcp()
			c = nm[host[0]].all_udp()
		
			print('{0}open Tcp ports for ip {1}'+host[0]+'{2} are {3}'+str(b)).format(YELLOW,RED,YELLOW,END)
		
			if b:
				for port in b :
					print('{0}service running at port {1}' + str(port) + ' {2}is {3}' + a['scan'][host[0]]['tcp'][port]['name']+'{4}').format(WHITE,RED,WHITE,BLUE,END)
					
			print('{0}open udp ports for ip {1}'+host[0]+'{2} are {3}'+str(c)).format(YELLOW,RED,YELLOW,END)
			if c:
				for port in c :
					print('{0}service running at port {1}' + str(port) + '{2} is {3}' + a['scan'][host[0]]['udp'][port]['name']+'{5}').format(WHITE,RED,WHITE,BLUE,END)
		except:
			continue
			
	
