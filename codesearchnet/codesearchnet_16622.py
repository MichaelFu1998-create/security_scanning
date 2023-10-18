def send(self):
        """
        Send a verification email to the user.
        """
        context = {
            "verification_url": app_settings.EMAIL_VERIFICATION_URL.format(
                key=self.key
            )
        }

        email_utils.send_email(
            context=context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email.email],
            subject=_("Please Verify Your Email Address"),
            template_name="rest_email_auth/emails/verify-email",
        )

        logger.info(
            "Sent confirmation email to %s for user #%d",
            self.email.email,
            self.email.user.id,
        )