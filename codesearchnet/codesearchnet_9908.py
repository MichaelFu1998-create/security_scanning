def cleanup(self):
        """Deletes this worker's subscription."""
        if self.subscription:
            logger.info("Deleting worker subscription...")
            self.subscriber_client.delete_subscription(self.subscription)