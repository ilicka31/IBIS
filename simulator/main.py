from flask import Flask
from Api.Farm import farm
from Api.Control import control
from Api.Emergency import emergency
from Simulator.Simulator import Simulator

app = Flask(__name__)
app.register_blueprint(farm, url_prefix='/farm')
app.register_blueprint(control, url_prefix='/control')
app.register_blueprint(emergency, url_prefix='/emergency')

if __name__ == '__main__':
    Simulator().start()
    app.run(host='0.0.0.0', port=5000)
