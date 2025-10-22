import threading
import time
import yaml
import random
from Model.FarmState import FarmState
from Simulator.logger import setup_logger

logger = setup_logger("Simulator")

class Simulator:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.farms = {
           "farm1" : FarmState(),
           "farm2" : FarmState()
        }
        self.event = threading.Event()
        self.event.set()
        self.load_config()

    def load_config(self):
        try:
            with open('config.yaml') as f:
                config = yaml.safe_load(f)
            self.update_interval = config['update_interval']
            self.temp_var = config['temperature_variation']
            self.humid_var = config['humidity_variation']
            self.soil_var = config['soil_moisture_variation']
            logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load config.yaml: {e}")
            self.update_interval = 2
            self.temp_var = 0.5
            self.humid_var = 1
            self.soil_var = 2

    def simulate(self):
        while True:
            if self.event.is_set():
                for farm_id, state in self.farms.items():
                    state.temperature += random.uniform(-self.temp_var, self.temp_var)
                    state.humidity += random.uniform(-self.humid_var, self.humid_var)
                    state.soil_moisture += random.uniform(-self.soil_var, self.soil_var)
                    state.soil_moisture = max(0, min(100, state.soil_moisture))

                    logger.info(f"{farm_id} Updated temperature: {state.temperature:.2f}°C")
                    logger.info(f"{farm_id} Updated humidity: {state.humidity:.2f}%")
                    logger.info(f"{farm_id} Updated soil moisture: {state.soil_moisture:.2f}%")

            time.sleep(self.update_interval)

    def start(self):
        logger.info("Starting simulation thread")
        threading.Thread(target=self.simulate, daemon=True).start()

    def emergency_stop(self):
        logger.warning("Emergency stop triggered")
        self.event.clear()

    def resume(self):
        logger.info("Simulation resumed")
        self.event.set()
