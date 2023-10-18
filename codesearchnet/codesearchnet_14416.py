def start_watching(self):
        """ Begins watching etcd for changes. """
        # Don't create a new watcher thread if we already have one running
        if self.watcher and self.watcher.is_alive():
            return

        # Create a new watcher thread and start it
        self.watcher = Watcher()
        self.watcher.start()