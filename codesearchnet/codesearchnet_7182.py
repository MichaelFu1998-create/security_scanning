async def leave_conversation(self, conv_id):
        """Leave a conversation.

        Args:
            conv_id (str): ID of conversation to leave.
        """
        logger.info('Leaving conversation: {}'.format(conv_id))
        await self._conv_dict[conv_id].leave()
        del self._conv_dict[conv_id]