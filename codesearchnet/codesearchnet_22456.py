def run(self):
        """Runs the consumer."""
        self.log.debug('consumer is running...')

        self.running = True
        while self.running:
            self.upload()

        self.log.debug('consumer exited.')