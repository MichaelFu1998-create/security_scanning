def is_already_running(self):
        """Return True if lock exists and has not timed out."""
        redis_key = self.CELERY_LOCK.format(task_id=self.task_identifier)
        return self.celery_self.backend.client.exists(redis_key)