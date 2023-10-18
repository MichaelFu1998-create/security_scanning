def run(self, next_task):
        """Wait for the event, run the task, trigger the next task."""
        self.event.wait()
        self.task()
        self.event.clear()

        next_task.event.set()