def get_watcher(self):
        """
        Return a etcd watching generator which yields events as they happen.

        """
        if not self.watching:
            raise StopIteration()
        return self.client.eternal_watch(self.prefix, recursive=True)