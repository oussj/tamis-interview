from exercise.queue import PriorityQueue
from exercise.api import API

from exercise.pool import DevicePool
from exercise.worker import Worker

# The actual program
if __name__ == "__main__":
    print("Starting the scheduler")

    pool = DevicePool()
    queue = PriorityQueue()

    # Running the api should not block. You should run it asynchronously
    # using threading, asyncio, or any other library you see fit.
    api = API()
    # TODO: api.run_async()

    # TODO:
    worker = Worker()
    worker.run()
