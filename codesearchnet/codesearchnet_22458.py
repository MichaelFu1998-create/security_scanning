def next(self):
        """Return the next batch of items to upload."""
        queue = self.queue
        items = []
        item = self.next_item()
        if item is None:
            return items

        items.append(item)
        while len(items) < self.upload_size and not queue.empty():
            item = self.next_item()
            if item:
                items.append(item)

        return items