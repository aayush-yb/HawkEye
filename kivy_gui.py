from scanner import *


import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup


class MyApp(App):

	#title of the Application Window
	title="Network Scanner"

	
	def __init__(self):
		super(MyApp, self).__init__()

		#getting the basic info like default interface and MAC address of the default interface
		self.defaultInterface=getDefaultInterface();
		self.defaultInterfaceMAC=getDefaultInterfaceMAC(self.defaultInterface)

	def attemptDefaultGateway(self,button):
		self.defaultGatewayIP.text=getGatewayIP(False)


	def setConnectedDevicesList(self):
		self.layout_connected_devices.clear_widgets()
		
		#setting the title of the connected devices list
		self.layout_connected_devices.add_widget(Label(text="IP Address"))
		self.layout_connected_devices.add_widget(Label(text="MAC Address"))
		self.layout_connected_devices.add_widget(Label(text="Vendor"))

		#adding them to the list
		for ip,mac,vendor in self.connectedNodes:
			self.layout_connected_devices.add_widget(Label(text=ip))
			self.layout_connected_devices.add_widget(Label(text=mac))
			self.layout_connected_devices.add_widget(Label(text=vendor))

	#Once the un-dismissable popup opens, we start getting the nodes that are connected
	def connectedNodesSetter(self,instance):
		self.connectedNodes=getNodes()
		
		#adding NIC Vendor details to the fetched details			
		for x in self.connectedNodes:
			x.append(resolveMac(x[1]))

		instance.dismiss()

		#Now we set the details box in the Application with the details fetched
		self.setConnectedDevicesList()


	#this displays the pop_up once the app opens
	def getConnectedDevices(self,button):
		popup = Popup(title='Please wait..',content=Label(text='Fetching connected devices'),size_hint=(None,None),size=(400, 200),auto_dismiss=False)
		popup.bind(on_open=self.connectedNodesSetter)		
		popup.open()


	def build(self):
		main_layout = BoxLayout(orientation='vertical',padding=[10,10,10,10])
		
		#Child layout for default Interface and its MAC Address 		
		layoutInterface=GridLayout(padding=[0,0,0,10],cols=2,size_hint=(1,0.5))
		
		layoutInterface.add_widget(Label(text='Default Interface'))
		layoutInterface.add_widget(Label(text=''+self.defaultInterface))

		layoutInterface.add_widget(Label(text='Default Interface MAC Address'))
		layoutInterface.add_widget(Label(text=self.defaultInterfaceMAC))

		main_layout.add_widget(layoutInterface)

		#Child layout for the default gateway IP Address
		layoutGatewayIP=GridLayout(cols=3,padding=[0,10,0,10],size_hint=(1,0.2))

		layoutGatewayIP.add_widget(Label(text='Default Gateway IP Address'))
		self.defaultGatewayIP=TextInput(multiline=False,text="",hint_text="Enter Default Gateway here",padding=[10,15,10,10])

		layoutGatewayIP.add_widget(self.defaultGatewayIP)
		
		self.buttonAutogatewayIP=Button(text="Get Default gateway Automatically",on_press=self.attemptDefaultGateway)
		layoutGatewayIP.add_widget(self.buttonAutogatewayIP)
		main_layout.add_widget(layoutGatewayIP)


		#Button that will load the devices that are connected
		buttonGetConnectedNodes=Button(text="Get the devices connected",size_hint=(1,0.2),on_press=self.getConnectedDevices);
		main_layout.add_widget(buttonGetConnectedNodes)


		#This box displays the details of the devices that are connected
		layout_details=GridLayout(cols=3)
		layout_details.add_widget(Label(text="IP"))
		layout_details.add_widget(Label(text="MAC Address"))
		layout_details.add_widget(Label(text="Vendor"))
		self.layout_connected_devices=layout_details

		main_layout.add_widget(layout_details)

		return main_layout

if __name__=='__main__':
	MyApp().run()
