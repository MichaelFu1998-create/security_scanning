def clean(self):
        """When receiving the filled out form, check for valid access."""
        cleaned_data = super(AuthForm, self).clean()
        user = self.get_user()
        if self.staff_only and (not user or not user.is_staff):
            raise forms.ValidationError('Sorry, only staff are allowed.')
        if self.superusers_only and (not user or not user.is_superuser):
            raise forms.ValidationError('Sorry, only superusers are allowed.')
        return cleaned_data