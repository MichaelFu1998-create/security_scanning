def send_confirmation(self):
        """
        Send a verification email for the email address.
        """
        confirmation = EmailConfirmation.objects.create(email=self)
        confirmation.send()