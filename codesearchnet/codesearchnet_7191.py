def upgrade_name(self, user_):
        """Upgrade name type of this user.

        Google Voice participants often first appear with no name at all, and
        then get upgraded unpredictably to numbers ("+12125551212") or names.

        Args:
            user_ (~hangups.user.User): User to upgrade with.
        """
        if user_.name_type > self.name_type:
            self.full_name = user_.full_name
            self.first_name = user_.first_name
            self.name_type = user_.name_type
            logger.debug('Added %s name to User "%s": %s',
                         self.name_type.name.lower(), self.full_name, self)