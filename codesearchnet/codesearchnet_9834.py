def clean_password(self):
        """Check that the password is valid."""
        value = self.cleaned_data.get('password')
        if value not in self.valid_passwords:
            raise forms.ValidationError('Incorrect password.')
        return value