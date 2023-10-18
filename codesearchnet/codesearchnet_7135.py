async def rename_conversation(self, rename_conversation_request):
        """Rename a conversation.

        Both group and one-to-one conversations may be renamed, but the
        official Hangouts clients have mixed support for one-to-one
        conversations with custom names.
        """
        response = hangouts_pb2.RenameConversationResponse()
        await self._pb_request('conversations/renameconversation',
                               rename_conversation_request, response)
        return response