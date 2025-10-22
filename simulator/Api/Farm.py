from flask import Blueprint, jsonify
from Simulator.Simulator import Simulator
from Simulator.logger import setup_logger

logger = setup_logger("API")
farm = Blueprint('farm', __name__)
sim = Simulator()

@farm.route('/<farm_id>', methods=['GET'])
def get_farm(farm_id):
    state = sim.farms.get(farm_id)
    return jsonify({
        'temperature': state.temperature,
        'humidity': state.humidity,
        'soil_moisture': state.soil_moisture
    })
