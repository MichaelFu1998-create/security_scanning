def _random_token(self, bits=128):
        """
        Generates a random token, using the url-safe base64 alphabet.
        The "bits" argument specifies the bits of randomness to use.
        """
        alphabet = string.ascii_letters + string.digits + '-_'
        # alphabet length is 64, so each letter provides lg(64) = 6 bits
        num_letters = int(math.ceil(bits / 6.0))
        return ''.join(random.choice(alphabet) for i in range(num_letters))