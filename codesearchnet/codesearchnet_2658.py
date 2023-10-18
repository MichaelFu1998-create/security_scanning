def process(self, tup):
    """Process a single tuple of input

    We add the (time, tuple) pair into our current_tuples. And then look for expiring
    elemnents
    """
    curtime = int(time.time())
    self.current_tuples.append((tup, curtime))
    self._expire(curtime)