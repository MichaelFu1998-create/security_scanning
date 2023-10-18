def can_send(self, user, notice_type):
        """
        Determines whether this backend is allowed to send a notification to
        the given user and notice_type.
        """
        from notification.models import NoticeSetting
        return NoticeSetting.for_user(user, notice_type, self.medium_id).send