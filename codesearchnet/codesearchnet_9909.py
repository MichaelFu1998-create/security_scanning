def _get_or_create_subscription(self):
        """Workers all share the same subscription so that tasks are
        distributed across all workers."""
        topic_path = self._get_topic_path()
        subscription_name = '{}-{}-shared'.format(
            PUBSUB_OBJECT_PREFIX, self.name)
        subscription_path = self.subscriber_client.subscription_path(
            self.project, subscription_name)

        try:
            self.subscriber_client.get_subscription(subscription_path)
        except google.cloud.exceptions.NotFound:
            logger.info("Creating shared subscription {}".format(
                subscription_name))
            try:
                self.subscriber_client.create_subscription(
                    subscription_path, topic=topic_path)
            except google.cloud.exceptions.Conflict:
                # Another worker created the subscription before us, ignore.
                pass

        return subscription_path