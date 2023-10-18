def get_activity(self, name):
        """
        Retrieve an activity given its name.

        :param name: The name of the activity.

        :returns: The activity.
        """

        return [a for a in self.activities if a.name == name][0]