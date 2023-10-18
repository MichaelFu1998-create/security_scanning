def clean(self):
        """
        Validate that an event with this name on this date does not exist.
        """
        cleaned = super(EventForm, self).clean()
        if Event.objects.filter(name=cleaned['name'], start_date=cleaned['start_date']).count():
            raise forms.ValidationError(u'This event appears to be in the database already.')
        return cleaned