def request_roster(self, version = None):
        """Request roster from server.

        :Parameters:
            - `version`: if not `None` versioned roster will be requested
              for given local version. Use "" to request full roster.
        :Types:
            - `version`: `unicode`
        """
        processor = self.stanza_processor
        request = Iq(stanza_type = "get")
        request.set_payload(RosterPayload(version = version))
        processor.set_response_handlers(request,
                                    self._get_success, self._get_error)
        processor.send(request)