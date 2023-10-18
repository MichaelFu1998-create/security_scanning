def ready(self):
        """
        Perform other one-time initialization steps.
        """
        from enterprise.signals import handle_user_post_save
        from django.db.models.signals import pre_migrate, post_save

        post_save.connect(handle_user_post_save, sender=self.auth_user_model, dispatch_uid=USER_POST_SAVE_DISPATCH_UID)
        pre_migrate.connect(self._disconnect_user_post_save_for_migrations)