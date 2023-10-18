def unlocked(self):
        """ Is the store unlocked so that I can decrypt the content?
        """
        if self.password is not None:
            return bool(self.password)
        else:
            if (
                "UNLOCK" in os.environ
                and os.environ["UNLOCK"]
                and self.config_key in self.config
                and self.config[self.config_key]
            ):
                log.debug("Trying to use environmental " "variable to unlock wallet")
                self.unlock(os.environ.get("UNLOCK"))
                return bool(self.password)
        return False