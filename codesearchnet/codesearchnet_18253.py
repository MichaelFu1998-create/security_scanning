def start_timer(self, duration, func, *args):
        """
        Schedules a function to be called after some period of time.

        * duration - time in seconds to wait before firing
        * func - function to be called
        * args - arguments to pass to the function
        """
        t = threading.Timer(duration, self._timer_callback, (func, args))
        self._timer_callbacks[func] = t
        t.start()
        self.log.info("Scheduled call to %s in %ds", func.__name__, duration)