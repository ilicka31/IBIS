from flask import Blueprint, request, jsonify
from Simulator.Simulator import Simulator
from Simulator.logger import setup_logger


logger = setup_logger("API")
control = Blueprint('control', __name__)
sim = Simulator()

@control.route('/<farm_id>/irrigation', methods=['PUT'])
def set_irrigation(farm_id):
    state = sim.farms.get(farm_id)
    if not state:
        return jsonify({'error': 'Farm not found'}), 404
    logger.info(f"PUT /control/irrigation → {request.json}")
    state.irrigation = request.json.get('irrigation')
    return jsonify({'irrigation': state.irrigation})

@control.route('/<farm_id>/door', methods=['PUT'])
def set_door(farm_id):
    state = sim.farms.get(farm_id)
    if not state:
        return jsonify({'error': 'Farm not found'}), 404
    state.greenhouse_door = request.json.get('door')
    return jsonify({'greenhouse_door': state.greenhouse_door})
