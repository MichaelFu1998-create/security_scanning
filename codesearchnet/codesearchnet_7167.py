def _on_watermark_notification(self, notif):
        """Handle a watermark notification."""
        # Update the conversation:
        if self.get_user(notif.user_id).is_self:
            logger.info('latest_read_timestamp for {} updated to {}'
                        .format(self.id_, notif.read_timestamp))
            self_conversation_state = (
                self._conversation.self_conversation_state
            )
            self_conversation_state.self_read_state.latest_read_timestamp = (
                parsers.to_timestamp(notif.read_timestamp)
            )
        # Update the participants' watermarks:
        previous_timestamp = self._watermarks.get(
            notif.user_id,
            datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
        )
        if notif.read_timestamp > previous_timestamp:
            logger.info(('latest_read_timestamp for conv {} participant {}' +
                         ' updated to {}').format(self.id_,
                                                  notif.user_id.chat_id,
                                                  notif.read_timestamp))
            self._watermarks[notif.user_id] = notif.read_timestamp