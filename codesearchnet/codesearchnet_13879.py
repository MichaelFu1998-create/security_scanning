def callback(self, *incoming):
        """
        Gets called by the CallbackManager if a new message was received 
        """
        message = incoming[0]
        if message:
            address, command = message[0], message[2]
            profile = self.get_profile(address)
            if profile is not None:
                try:
                    getattr(profile, command)(self, message)
                except AttributeError:
                    pass