def _get_event_request_header(self):
        """Return EventRequestHeader for conversation."""
        otr_status = (hangouts_pb2.OFF_THE_RECORD_STATUS_OFF_THE_RECORD
                      if self.is_off_the_record else
                      hangouts_pb2.OFF_THE_RECORD_STATUS_ON_THE_RECORD)
        return hangouts_pb2.EventRequestHeader(
            conversation_id=hangouts_pb2.ConversationId(id=self.id_),
            client_generated_id=self._client.get_client_generated_id(),
            expected_otr=otr_status,
            delivery_medium=self._get_default_delivery_medium(),
        )