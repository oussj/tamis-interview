from flask import Flask
from exercise.pool import DevicePool

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

        
    def hello_world(self):
        return "Hello"
    
    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))

    def run(self):
        self.add_endpoint(endpoint='/test', endpoint_name='test', handler=EndpointAction(self.hello_world))
        self.app.run()
