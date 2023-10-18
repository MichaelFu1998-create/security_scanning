def _get_or_create_subscription(self):
        """In a broadcast queue, workers have a unique subscription ensuring
        that every worker recieves a copy of every task."""
        topic_path = self._get_topic_path()
        subscription_name = '{}-{}-{}-worker'.format(
            queue.PUBSUB_OBJECT_PREFIX, self.name, uuid4().hex)
        subscription_path = self.subscriber_client.subscription_path(
            self.project, subscription_name)

        try:
            self.subscriber_client.get_subscription(subscription_path)
        except google.cloud.exceptions.NotFound:
            logger.info("Creating worker subscription {}".format(
                subscription_name))
            self.subscriber_client.create_subscription(
                subscription_path, topic_path)

        return subscription_path