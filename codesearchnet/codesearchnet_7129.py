async def get_entity_by_id(self, get_entity_by_id_request):
        """Return one or more user entities.

        Searching by phone number only finds entities when their phone number
        is in your contacts (and not always even then), and can't be used to
        find Google Voice contacts.
        """
        response = hangouts_pb2.GetEntityByIdResponse()
        await self._pb_request('contacts/getentitybyid',
                               get_entity_by_id_request, response)
        return response