def pre_parse_and_validate(self, bpmn, filename):
        """
        A subclass can override this method to provide additional parseing or
        validation. It should call the parent method first.

        :param bpmn: an lxml tree of the bpmn content

        :param filename: the source file name

        This must return the updated bpmn object (or a replacement)
        """
        bpmn = self._call_editor_hook(
            'pre_parse_and_validate', bpmn, filename) or bpmn

        return bpmn