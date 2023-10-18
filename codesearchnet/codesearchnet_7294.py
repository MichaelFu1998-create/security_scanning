def update_local_repo_async(self, task_queue, force=False):
        """Local repo updating suitable for asynchronous, parallel execution.
        We still need to run `ensure_local_repo` synchronously because it
        does a bunch of non-threadsafe filesystem operations."""
        self.ensure_local_repo()
        task_queue.enqueue_task(self.update_local_repo, force=force)