def confirm(self):
        """
        Mark the instance's email as verified.
        """
        self.email.is_verified = True
        self.email.save()

        signals.email_verified.send(email=self.email, sender=self.__class__)

        logger.info("Verified email address: %s", self.email.email)