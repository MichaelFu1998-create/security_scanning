def clean_notify(self):
        """
        Clean the notify_on_enrollment field.
        """
        return self.cleaned_data.get(self.Fields.NOTIFY, self.NotificationTypes.DEFAULT)