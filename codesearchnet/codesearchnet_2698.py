def register_timer_task_in_sec(self, task, second):
    """Registers a new timer task

    :param task: function to be run at a specified second from now
    :param second: how many seconds to wait before the timer is triggered
    """
    # Python time is in float
    second_in_float = float(second)
    expiration = time.time() + second_in_float
    heappush(self.timer_tasks, (expiration, task))