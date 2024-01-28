from flask import Flask
from exercise.pool import DevicePool
from flask import Flask, request, jsonify
import threading
from exercise.errors import ErrorDeviceAlreadyExists, ErrorDeviceNotFound
from exercise.device import Device

# Flask class implementation from https://stackoverflow.com/questions/40460846/using-flask-inside-class
class EndpointAction(object):

    def __init__(self, action):
        self.action = action

    def __call__(self, *args):
        message = self.action()
    
        return message
        
class API:
    """This class is supposed to contain the web server.
    API.run should start the server.
    """
    app = None
    
    def __init__(self, device_pool: DevicePool):
        self.app = Flask("api")
        self.device_pool = device_pool

        
    def add_device_handler(self):
        data = request.json
        device_id = data.get('device_id')
        device_type = data.get('device_type')
        device_address = data.get('device_address')
        device_size = data.get('device_size')
        device_state = data.get('device_state')

        try:
            if device_id and device_type and device_size is not None:
                device = Device(device_id, device_address, device_type, device_size, device_state)
                self.device_pool.add(device)
                return jsonify({"message": f"Device {device_id} added."}), 200
            return jsonify({"error": "Invalid data"}), 400
        except ErrorDeviceAlreadyExists:
            return jsonify({"error": "Device already exists"}), 400

    
    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET']):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=methods)

    def run(self):
        self.add_endpoint(endpoint='/add_device', endpoint_name='add_device', handler=EndpointAction(self.add_device_handler), methods=['POST'])
        self.app.run()
