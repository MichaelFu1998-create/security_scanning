def step(self, other_pub):
        """
        Perform a rachted step, calculating a new shared secret from the public key and
        deriving new chain keys from this secret.

        New Diffie-Hellman calculations are only performed if the public key is different
        from the previous one.

        :param other_pub: A bytes-like object encoding the public key of the other
            Diffie-Hellman ratchet to synchronize with.
        """

        if self.triggersStep(other_pub):
            self.__wrapOtherPub(other_pub)
            self.__newRootKey("receiving")

            self.__newRatchetKey()

            self.__newRootKey("sending")