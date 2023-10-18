def send_duplicate_notification(self):
        """
        Send a notification about a duplicate signup.
        """
        email_utils.send_email(
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            subject=_("Registration Attempt"),
            template_name="rest_email_auth/emails/duplicate-email",
        )

        logger.info("Sent duplicate email notification to: %s", self.email)