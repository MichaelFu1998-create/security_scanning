def _get_default_delivery_medium(self):
        """Return default DeliveryMedium to use for sending messages.

        Use the first option, or an option that's marked as the current
        default.
        """
        medium_options = (
            self._conversation.self_conversation_state.delivery_medium_option
        )
        try:
            default_medium = medium_options[0].delivery_medium
        except IndexError:
            logger.warning('Conversation %r has no delivery medium', self.id_)
            default_medium = hangouts_pb2.DeliveryMedium(
                medium_type=hangouts_pb2.DELIVERY_MEDIUM_BABEL
            )
        for medium_option in medium_options:
            if medium_option.current_default:
                default_medium = medium_option.delivery_medium
        return default_medium