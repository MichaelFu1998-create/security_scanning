def reset_lock(self):
        """Removed the lock regardless of timeout."""
        redis_key = self.CELERY_LOCK.format(task_id=self.task_identifier)
        self.celery_self.backend.client.delete(redis_key)