import random
import time
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Any


class DeviceState(Enum):
    UP = "UP"


@dataclass
class Device:
    id: str
    address: str
    type: str
    size: int
    state: DeviceState = None

    def send(self, instructions: Any):
        call_device(self.id)
        return random.getrandbits(self.size)
    
    def up(self):
        self.state = DeviceState.UP
        
    def down(self):
        self.state = None


# The following code is here to mock calls to the devices
# We register calls to each device and we respond random bitstrings

device_calls = defaultdict(int)


def call_device(id: str):
    device_calls[id] += 1
    time.sleep(2 * device_calls[id])
    device_calls[id] -= 1
    return random.getrandbits(10)
