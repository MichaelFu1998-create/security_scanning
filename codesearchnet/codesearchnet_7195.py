def _add_user_from_conv_part(self, conv_part):
        """Add or upgrade User from ConversationParticipantData."""
        user_ = User.from_conv_part_data(conv_part, self._self_user.id_)

        existing = self._user_dict.get(user_.id_)
        if existing is None:
            logger.warning('Adding fallback User with %s name "%s"',
                           user_.name_type.name.lower(), user_.full_name)
            self._user_dict[user_.id_] = user_
            return user_
        else:
            existing.upgrade_name(user_)
            return existing