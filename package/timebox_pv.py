import paho.mqtt.client as mqtt
import config
import json
import time
'''
    Test the mqtt daemon by sending various contents
'''

bat = 0.0
pv = 0.0
grid = 0.0

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+' '+str(msg.payload))
    
    global bat,pv,grid

    if (msg.topic == 'fhem/PV_Anlage_1/Home_own_consumption_from_battery'):
        bat = float(msg.payload)
    elif (msg.topic == 'fhem/PV_Anlage_1/Home_own_consumption_from_PV'):
        pv = float(msg.payload)
    elif (msg.topic == 'fhem/PV_Anlage_1/Home_own_consumption_from_grid'):
        grid = float(msg.payload)
    else:
        return

    if (grid <= 20):
        if (bat > 0):
            client.publish(config.mqtt_topic+"/in", payload=json.dumps({'action': "show_clock", 'color': 'yellow'}))
        else:
            client.publish(config.mqtt_topic+"/in", payload=json.dumps({'action': 'show_clock', 'color': 'green'}))
    elif (grid < -10):
        client.publish(config.mqtt_topic+"/in", payload=json.dumps({'action': 'show_clock', 'color': 'blue'}))
    else:
        client.publish(config.mqtt_topic+"/in", payload=json.dumps({'action': "show_clock", 'color': 'red'}))

client.on_connect = on_connect
client.on_message = on_message

client.connect(config.mqtt_server[0], config.mqtt_server[1], 60)

color_png = 'iVBORw0KGgoAAAANSUhEUgAAAAsAAAALCAYAAACprHcmAAAACXBIWXMAAA4mAAAN/wHwU+XzAAAAXElEQVQYlc2PQQ6AQAgDB1/en48HdjVr9qA3IQRKS1IQNKiMVBpqYoz26MGHOAAqz3XtxQWYvabSRNVNaBCGZ+4yWTBOYgq1Md1jH1wPXjZkGRw2+n48+DZ+Ij4BeddPVF7LZ+sAAAAASUVORK5CYII='
gif = 'R0lGODlhCwALAKECAAAAAP8AAP///////yH/C05FVFNDQVBFMi4wAwEAAAAh/hFDcmVhdGVkIHdpdGggR0lNUAAh+QQBCgACACwAAAAACwALAAACCoSPqcvtGZ6c1BUAIfkEAQoAAwAsAAAAAAsACwAAAg+Ej6nLFv2ekoCiCJverAAAIfkEAQoAAwAsAAAAAAsACwAAAg+Ej6kaC22gY0lOJC2+XBUAIfkEAQoAAwAsAAAAAAsACwAAAg+Ejwmhm9yihE9aRU0++xYAIfkEAQoAAwAsAAAAAAsACwAAAg+EHXep2A9jZJDKi4FdbxcAIfkEAQoAAwAsAAAAAAsACwAAAgwMjmjJ7Q+jnJQuFwoAIfkEAQoAAwAsAAAAAAsACwAAAgqEj6nL7Q+jnKAAACH5BAEKAAMALAAAAAALAAsAAAIKhI+py+0Po5ygAAA7'

print client.subscribe([("fhem/PV_Anlage_1/Home_own_consumption_from_battery",1),("fhem/PV_Anlage_1/Home_own_consumption_from_grid",1),("fhem/PV_Anlage_1/Home_own_consumption_from_PV",1)])




client.publish(config.mqtt_topic+'/in', payload=json.dumps({'action': 'show_clock', 'color': 'green'}))
time.sleep(3)
client.loop_forever()


"""
    Color name : http://pillow.readthedocs.io/en/3.1.x/reference/ImageColor.html#module-PIL.ImageColor
        Hexadecimal color specifiers, given as #rgb or #rrggbb. For example, #ff0000 specifies pure red.
        Common HTML color names
        4 LSB bits are dropped for each color channel 
"""
