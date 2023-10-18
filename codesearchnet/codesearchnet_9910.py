def enqueue(self, f, *args, **kwargs):
        """Enqueues a function for the task queue to execute."""
        task = Task(uuid4().hex, f, args, kwargs)
        self.storage.put_task(task)
        return self.enqueue_task(task)