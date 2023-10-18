def _boundary(self):
        """ Returns a random string to use as the boundary for a message.
        
        Returns:
            string. Boundary
        """
        boundary = None
        try:
            import uuid
            boundary = uuid.uuid4().hex
        except ImportError:
            import random, sha
            bits = random.getrandbits(160)
            boundary = sha.new(str(bits)).hexdigest()
        return boundary