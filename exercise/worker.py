from exercise.device import call_device
from exercise.pool import DevicePool
from exercise.queue import PriorityQueue
import time

from exercise.utils import handle_result

class Worker:
    def __init__(self, device_pool: DevicePool, job_queue: PriorityQueue):
        self.device_pool = device_pool
        self.job_queue = job_queue
        self.running = False

    def process_job(self, job):
        """send the job to the right device"""
        print(f"Processing job {job.id}...")
        try:

            
            device = self.device_pool.get_non_busy_device(job.device_type)
            device.up()
            response_code = call_device(device.id)
            job.result = response_code
            device.down()
            
            handle_result(job)
            
            return response_code
        except Exception as e:
            # TODO : retrieve old priority and push job back to queue
            # self.job_queue.push(job)
            print(e)
            print(f"Something went wrong during execution of job {job.id}.")

    def run(self):
        """wait for new jobs on the queue and send them to the right device"""
        self.running = True
        while self.running:
            print("Checking for new jobs...")
            job = self.job_queue.pop()
            if job:
                response_code = self.process_job(job)
                print(f"Job {job.id} processed with response code {response_code}.")
            else:
                # No jobs in the queue, so wait for a bit before checking again
                time.sleep(1)  # Sleeps for 1 second; adjust as needed

    def stop(self):
        self.running = False
    
