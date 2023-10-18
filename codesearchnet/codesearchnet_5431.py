def pre_parse_and_validate_signavio(self, bpmn, filename):
        """
        This is the Signavio specific editor hook for pre-parsing and
        validation.

        A subclass can override this method to provide additional parseing or
        validation. It should call the parent method first.

        :param bpmn: an lxml tree of the bpmn content

        :param filename: the source file name

        This must return the updated bpmn object (or a replacement)
        """
        self._check_for_disconnected_boundary_events_signavio(bpmn, filename)
        self._fix_call_activities_signavio(bpmn, filename)
        return bpmn