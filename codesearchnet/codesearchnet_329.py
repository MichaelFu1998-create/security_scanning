def offer(self, p, e: Event):
        """
        Offer a new event ``s`` at point ``p`` in this queue.
        """
        existing = self.events_scan.setdefault(
                p, ([], [], [], []) if USE_VERTICAL else
                   ([], [], []))
        # Can use double linked-list for easy insertion at beginning/end
        '''
        if e.type == Event.Type.END:
            existing.insert(0, e)
        else:
            existing.append(e)
        '''

        existing[e.type].append(e)