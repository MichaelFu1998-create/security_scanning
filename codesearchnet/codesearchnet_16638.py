def handle(self, *args, **kwargs):
        """
        Handle execution of the command.
        """
        cutoff = timezone.now()
        cutoff -= app_settings.CONFIRMATION_EXPIRATION
        cutoff -= app_settings.CONFIRMATION_SAVE_PERIOD

        queryset = models.EmailConfirmation.objects.filter(
            created_at__lte=cutoff
        )

        count = queryset.count()

        queryset.delete()

        if count:
            self.stdout.write(
                self.style.SUCCESS(
                    "Removed {count} old email confirmation(s)".format(
                        count=count
                    )
                )
            )
        else:
            self.stdout.write("No email confirmations to remove.")