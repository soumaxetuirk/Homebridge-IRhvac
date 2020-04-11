import time
import csv
import pickle
import json
import paho.mqtt.client as mqtt

def command(dataObj):
    json_data = json.dumps(dataObj)
    cmnd = 'IRhvac '+json_data
    client.publish("cmnd/light_bulb/IRhvac",(json_data))
    print(cmnd)   
    with open("ac.json", 'w') as f:
        json.dump(dataObj, f)
    
def on_connect(client, userdata, flags, rc):
    client.subscribe([("py/ac/active",0),("py/ac/init",0),("py/ac/state",0),("py/ac/temp",0),("py/ac/fan",0),("py/ac/swing",0)])
    print ('Connection done')
    global jdata
    with open("ac.json", 'r') as f:
        jdata = json.load(f)
           
def on_message(client, userdata, msg):    
    topic = msg.topic
    mes = str(msg.payload.decode("utf-8"))
    if (topic == 'py/ac/active'):
        client.publish("py/ac_r/active",mes)
        if (mes == 'false'):
            active = 'off'
            jdata['Power'] = 'off'
        else:
            jdata['Power'] = 'on'
        time.sleep(0.5)
        command(jdata)
        
    elif (topic == 'py/ac/state'):
        jdata['Mode'] = mes
        client.publish("py/ac_r/state",mes)
    elif (topic == 'py/ac/temp'):
        jdata['Temp'] = mes
        client.publish("py/ac/active",'true')
        client.publish("py/ac_r/temp",mes)
    elif (topic == 'py/ac/fan'):
        fs = int (mes)
        client.publish("py/ac_r/fan",mes)
        if (0 < fs <= 25):
            jdata['FanSpeed'] = 'low'
        elif (25 < fs <= 50):
            jdata['FanSpeed'] = 'mid'
        elif (50 < fs <= 75):
            jdata['FanSpeed'] = 'high'
        elif (75 < fs):
            jdata['FanSpeed'] = 'auto'
        else :
            pass       
    elif (topic == 'py/ac/swing'):
        jdata['SwingH'] = mes
        client.publish("py/ac/active",'true')
        client.publish("py/ac_r/swing",mes)
    else:
        if (jdata['Power'] == 'on'):
            client.publish("py/ac_r/active",'true')
        else:
           client.publish("py/ac_r/active",'false') 
        client.publish("py/ac_r/active",jdata['Power'])
        client.publish("py/ac_r/state",jdata['Mode'])
        client.publish("py/ac_r/swing",jdata['SwingH'])
        client.publish("py/ac_r/temp",jdata['Temp'])
        if (jdata['FanSpeed'] == 'high'):
            client.publish("py/ac_r/fan",65)
        elif (jdata['FanSpeed'] == 'mid'):
            client.publish("py/ac_r/fan",40)
        elif (jdata['FanSpeed'] == 'low'):
            client.publish("py/ac_r/fan",15)
        else :
            client.publish("py/ac_r/fan",85)
    
client = mqtt.Client()
client.connect("localhost",1883,60)
client.on_message = on_message
client.on_connect = on_connect
client.loop_forever()

