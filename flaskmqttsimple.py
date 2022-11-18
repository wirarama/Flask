from flask import Flask,render_template,request
from flask_mqtt import Mqtt
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('test')
    mqtt.subscribe('topik')
    mqtt.subscribe('relay')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(message.topic,message.payload.decode(),sep=":")
    if message.topic=="test":
        f = open("mqtttest.csv","a")
        f.write(message.payload.decode()+"\n")
        f.close()
        
@app.route('/relay', methods=['GET', 'POST'])
def relay():
    posted = None
    relay = [str(i+1) for i in range(4)]
    f = open("relay.log","r")
    mr = f.read()
    f.close()
    cr = []
    for i in mr:
        if i == "1":
            cr.append("checked")
        else:
            cr.append("")
    if request.method == 'POST':
        relaydata = request.form.getlist('relay')
        mr = ""
        cr = []
        for i in relay:
            if i in relaydata:
                mr+="1"
                cr.append("checked")
            else:
                mr+="0"
                cr.append("")
        f = open("relay.log","w")
        f.write(mr)
        f.close()
        mqtt.publish('relay',mr)
        posted = ["success","Relay sudah diupdate"]
    relay = list(zip(relay,cr))
    return render_template('relay.html',posted=posted,relay=relay)
        
@app.route('/visual')
def visualdata():
    from random import randint
    df = pd.read_csv('mqtttest.csv')
    df[['suhu','kelembaban']].plot()
    data = df.describe().astype(str).values.tolist()
    index = df.describe().index.tolist()
    data = list(zip(index,data))
    plt.savefig('static/visual.png')
    return render_template('visual.html',data=data,random=randint(100,999))
        
@app.route('/', methods=['GET', 'POST'])
def showdata():
    posted = None
    if request.method == 'POST':
        try:
            mqtt.publish('topik',request.form['pesan'])
            posted = ["success","Pesan:"+request.form['pesan']+" terkirim"]
        except:
            posted = ["danger","Pesan:"+request.form['pesan']+" gagal terkirim"]
    df = pd.read_csv('mqtttest.csv')
    data = df.astype(str).values.tolist()
    return render_template('mqtt.html',data=data,posted=posted)

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.run()
