def enqueue_task(self, task):
        """Enqueues a task directly. This is used when a task is retried or if
        a task was manually created.

        Note that this does not store the task.
        """
        data = dumps(task)

        if self._async:
            self.publisher_client.publish(self.topic_path, data=data)
            logger.info('Task {} queued.'.format(task.id))
        else:
            unpickled_task = unpickle(data)
            logger.info(
                'Executing task {} synchronously.'.format(unpickled_task.id)
            )
            with measure_time() as summary, self.queue_context():
                unpickled_task.execute(queue=self)
                summary(unpickled_task.summary())

        return TaskResult(task.id, self)