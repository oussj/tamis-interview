from flask import Flask
from exercise.pool import DevicePool
from flask import Flask, request, jsonify
from exercise.errors import ErrorDeviceAlreadyExists, ErrorDeviceNotFound, ErrorJobAlreadyExists
from exercise.device import Device
from exercise.queue import PriorityQueue
from exercise.job import Job
import threading

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
    
    def __init__(self, device_pool: DevicePool, job_queue: PriorityQueue):
        self.app = Flask("api")
        self.device_pool = device_pool
        self.job_queue = job_queue
        self.add_endpoints()

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET']):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=methods)

    def add_endpoints(self):
        self.app.add_url_rule('/devices', 'add_device', EndpointAction(self.add_device_handler), methods=['POST'])
        self.app.add_url_rule('/devices', 'remove_device', EndpointAction(self.remove_device_handler), methods=['DELETE'])
        self.app.add_url_rule('/jobs', 'add_job', EndpointAction(self.add_job_handler), methods=['POST'])
        
    def add_device_handler(self):
        data = request.json
        device_id = data.get('id')
        device_type = data.get('type')
        device_address = data.get('address')
        device_size = data.get('size')

        try:
            if device_id and device_type and device_size is not None:
                device = Device(device_id, device_address, device_type, device_size)
                self.device_pool.add(device)
                return jsonify({"message": f"Device {device_id} added."}), 200
            return jsonify({"error": "Invalid data"}), 400
        except ErrorDeviceAlreadyExists:
            return jsonify({"error": "Device already exists"}), 400
        
    def add_job_handler(self):
        data = request.json
        job_id = data.get('id')
        job_user_id = data.get('user_id')
        job_device_type = data.get('device_type')
        job_program_id = data.get('program_id')
        
        try:
            if job_id and job_user_id and job_device_type and job_program_id is not None:
                job = Job(job_id, job_user_id, job_device_type, job_program_id)
                self.job_queue.push(job, job.priority)
                return jsonify({"message": f"Job {job_id} added."}), 200
            return jsonify({"error": "Invalid data"}), 400
        except ErrorJobAlreadyExists:
            return jsonify({"error": "Job already exists"}), 400

    def remove_device_handler(self):
        data = request.json
        device_id = data.get('id')

        try:
            if device_id:
                self.device_pool.remove(device_id)
                return jsonify({"message": f"Device {device_id} removed."}), 200
            return jsonify({"error": "Invalid device ID"}), 400
        except ErrorDeviceNotFound:
            return jsonify({"error": "Device not found"}), 404

    def run(self):
        self.app.run()
        
    def run_async(self):
        """Run the Flask app in a separate thread."""
        threading.Thread(target=self.app.run, kwargs={'use_reloader': False}).start()

