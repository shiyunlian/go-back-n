import time

class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")
    
    def timeout(self):
        elapsed_time = time.perf_counter() - self._start_time
        return elapsed_time > 0.5

# import time

# class Timer():
#     TIMER_STOP = -1
#     DURATION = 0.2
#     def __init__(self):
#         self._start_time = self.TIMER_STOP
#         self._duration = self.DURATION

#     # Starts the timer
#     def start(self):
#         if self._start_time == self.TIMER_STOP:
#             self._start_time = time.time()
#         print(self._start_time)

#     # Stops the timer
#     def stop(self):
#         if self._start_time != self.TIMER_STOP:
#             self._start_time = self.TIMER_STOP

#     # Determines whether the timer is runnning
#     def running(self):
#         return self._start_time != self.TIMER_STOP

#     # Determines whether the timer timed out
#     def timeout(self):
#         # if not self.running():
#         #     return False
#         # else:
#         print(time.time() - self._start_time)
#         return time.time() - self._start_time >= self._duration