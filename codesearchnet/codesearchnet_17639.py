def add_activity(self, activity):
        """
        Add an activity to the component.

        :param activity: The activity.
        """

        self.gl.structure.validate_account_names(
            activity.get_referenced_accounts())
        self.activities.append(activity)
        activity.set_parent_path(self.path)