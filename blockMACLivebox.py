#!/usr/bin/python3
import requests
import sys
import json
import base64


password="password"
auth=base64.b64encode("UsrAdmin:{}".format(password).encode("utf-8")).decode("utf-8")

hd={
	'Authorization':"Basic {}".format(auth),
	'Accept': 'application/json',
	'Host': '192.168.1.1',
	'Connection': 'Keep-Alive',
	'Accept-Encoding': 'gzip',
	'User-Agent': 'okhttp/3.5.0'
}

if len(sys.argv)==3:
	action=sys.argv[1]
	mac=sys.argv[2]
	current=requests.get('http://192.168.1.1/API/Services/ParentalCtrl/Devices',headers=hd)
	status=(True in [x["MAC"]==mac for x in json.loads(current.text)])
	devi={
	  "Status": "Enabled",
	  "MAC": mac
	}
	ad={
		"Status":"Enabled",
		"Start":"00:00",
		"End":"24:00",
		"Day":"All"
	}
	if action=="block":
		if not status:
			s=requests.post("http://192.168.1.1/API/Services/ParentalCtrl/Devices", json=devi,headers=hd)
			s=requests.post("http://192.168.1.1/API/Services/ParentalCtrl/Devices/{}/Schedules".format(mac.replace(":","")), json=ad,headers=hd)
	elif action=="unblock":
		if status:
			try:
				s=requests.delete("http://192.168.1.1/API/Services/ParentalCtrl/Devices/{}".format(mac.replace(":","")), headers=hd)
			except:
				pass
		
d=requests.get('http://192.168.1.1/API/Services/ParentalCtrl/Devices',headers=hd)

print(d.text)
