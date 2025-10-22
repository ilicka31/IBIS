from flask import Blueprint, request, jsonify
from Simulator.Simulator import Simulator
from Simulator.logger import setup_logger

logger = setup_logger("API")
emergency = Blueprint('emergency', __name__)
sim = Simulator()

@emergency.route('/', methods=['PUT'])
def toggle_emergency():
    logger.warning(f"PUT /emergency → {request.json}")
    status = request.json.get('emergency')
    if status:
        sim.emergency_stop()
    else:
        sim.resume()
    return jsonify({'emergency': status})
