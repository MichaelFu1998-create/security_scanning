def breakfast(self, message="Breakfast is ready", shout: bool = False):
        """Say something in the morning"""
        return self.helper.output(message, shout)