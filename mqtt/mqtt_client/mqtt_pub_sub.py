import requests, time
from paho.mqtt import client as mqtt_client
import mqtt_client.mqtt_config as config
from mqtt_client.states import farm_states
from mqtt_client.logger import setup_logger

endpoint = 'http://simulator:5000'
logger = setup_logger("MQTT")

def connect_mqtt(client_id):
    client = mqtt_client.Client(client_id)
    client.connect(config.broker, config.port)
    return client

def _publish(client, topic, message):
    client.publish(topic, message)
    logger.info(f"Published to {topic}: {float(message):.2f}")

def pull_data(client):
    while True:
        time.sleep(2)
        for farm_id, state in farm_states.items():
            try:

                r = requests.get(endpoint + '/farm/' + farm_id)
                if r.status_code == 200:
                    data = r.json()

                    for key in ['temperature', 'humidity', 'soil_moisture']:
                        if state[key] != data[key]:
                            state[key] = data[key]
                            _publish(client, config.topics[farm_id][key], data[key])

                    if data['soil_moisture'] < 20 and state['irrigation'] != 1:
                        requests.put(endpoint + '/control/' + farm_id + '/irrigation', json={'irrigation': 1})
                        state['irrigation'] = 1
                        _publish(client, config.topics[farm_id]['irrigation'], 1)
                        logger.info(f"🚨 Auto-control {farm_id}: Irrigation turned ON due to low soil moisture")

                    elif data['soil_moisture'] > 60 and state['irrigation'] != 0:
                        requests.put(endpoint + '/control/' + farm_id + '/irrigation', json={'irrigation': 0})
                        state['irrigation'] = 0
                        _publish(client, config.topics[farm_id]['irrigation'], 0)
                        logger.info("🚨 Auto-control {farm_id}: Irrigation turned OFF due to high soil moisture")

                    if data['temperature'] > 30 and state['greenhouse_door'] != 1:
                        requests.put(endpoint + '/control/'+ farm_id +'/door', json={'door': 1})
                        state['greenhouse_door'] = 1
                        _publish(client, config.topics[farm_id]['door'], 1)
                        logger.info("🚨 Auto-control {farm_id}: Door OPENED due to high temperature")

                    elif data['temperature'] < 18 and state['greenhouse_door'] != 0:
                        requests.put(endpoint + '/control/'+ farm_id +'/door', json={'door': 0})
                        state['greenhouse_door'] = 0
                        _publish(client, config.topics[farm_id]['door'], 0)
                        logger.info("🚨 Auto-control {farm_id}: Door CLOSED due to low temperature")

            except Exception as e:
                logger.error(f"{farm_id} Error in pull_data: {e}")

                    
def get_message(topic):
    client = connect_mqtt(f"listener_{topic}")
    _subscribe(client, topic)
    client.loop_start()
                 
def _subscribe(client, topic):
    def on_message(client, userdata, msg):
        value = int(msg.payload.decode())
        logger.info(f"Received control message on {msg.topic}: {value}")

        if msg.topic == config.topics['irrigation']:
            requests.put(endpoint + '/control/irrigation', json={'irrigation': value})
        elif msg.topic == config.topics['door']:
            requests.put(endpoint + '/control/door', json={'door': value})
        elif msg.topic == config.topics['emergency']:
            requests.put(endpoint + '/emergency', json={'emergency': value})

    client.subscribe(topic)
    client.on_message = on_message

