def next_item(self):
        """Get a single item from the queue."""
        queue = self.queue
        try:
            item = queue.get(block=True, timeout=5)
            return item
        except Exception:
            return None