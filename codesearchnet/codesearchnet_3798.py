def _auto_help_text(self, help_text):
        """Given a method with a docstring, convert the docstring
        to more CLI appropriate wording, and also disambiguate the
        word "object" on the base class docstrings.
        """
        # Delete API docs if there are any.
        api_doc_delimiter = '=====API DOCS====='
        begin_api_doc = help_text.find(api_doc_delimiter)
        if begin_api_doc >= 0:
            end_api_doc = help_text.rfind(api_doc_delimiter) + len(api_doc_delimiter)
            help_text = help_text[:begin_api_doc] + help_text[end_api_doc:]
        # Convert the word "object" to the appropriate type of
        # object being modified (e.g. user, organization).
        an_prefix = ('a', 'e', 'i', 'o')
        if not self.resource_name.lower().startswith(an_prefix):
            help_text = help_text.replace('an object',
                                          'a %s' % self.resource_name)
        if self.resource_name.lower().endswith('y'):
            help_text = help_text.replace(
                'objects',
                '%sies' % self.resource_name[:-1],
            )
        help_text = help_text.replace('object', self.resource_name)

        # Convert some common Python terms to their CLI equivalents.
        help_text = help_text.replace('keyword argument', 'option')
        help_text = help_text.replace('raise an exception',
                                      'abort with an error')

        # Convert keyword arguments specified in docstrings enclosed
        # by backticks to switches.
        for match in re.findall(r'`([\w_]+)`', help_text):
            option = '--%s' % match.replace('_', '-')
            help_text = help_text.replace('`%s`' % match, option)

        # Done; return the new help text.
        return help_text