from multiprocessing import Process
from flask import Flask
from mqtt_client import mqtt_pub_sub

app = Flask(__name__)

def start_processes():
    client = mqtt_pub_sub.connect_mqtt('farm_monitor')
    client.loop_start()
    Process(target=mqtt_pub_sub.pull_data, args=(client,)).start()

    for keyFarm in mqtt_pub_sub.config.topics:
        for key in ['irrigation', 'door', 'emergency']:
            topic = mqtt_pub_sub.config.topics[keyFarm][key]
            Process(target=mqtt_pub_sub.get_message, args=(topic,)).start()

if __name__ == '__main__':
    start_processes()
    app.run(host='0.0.0.0', port=5001)
