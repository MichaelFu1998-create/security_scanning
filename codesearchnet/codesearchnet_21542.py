def dinner(self, message="Dinner is served", shout: bool = False):
        """Say something in the evening"""
        return self.helper.output(message, shout)