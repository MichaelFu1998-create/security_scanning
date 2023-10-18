def _parse_revision_date(self):
        r"""Parse the ``\date`` command, falling back to getting the
        most recent Git commit date and the current datetime.

        Result is available from the `revision_datetime` attribute.
        """
        doc_datetime = None

        # First try to parse the \date command in the latex.
        # \date is ignored for draft documents.
        if not self.is_draft:
            date_command = LatexCommand(
                'date',
                {'name': 'content', 'required': True, 'bracket': '{'})
            try:
                parsed = next(date_command.parse(self._tex))
                command_content = parsed['content'].strip()
            except StopIteration:
                command_content = None
                self._logger.warning('lsstdoc has no date command')

            # Try to parse a date from the \date command
            if command_content is not None and command_content != r'\today':
                try:
                    doc_datetime = datetime.datetime.strptime(command_content,
                                                              '%Y-%m-%d')
                    # Assume LSST project time (Pacific)
                    project_tz = timezone('US/Pacific')
                    localized_datetime = project_tz.localize(doc_datetime)
                    # Normalize to UTC
                    doc_datetime = localized_datetime.astimezone(pytz.utc)

                    self._revision_datetime_source = 'tex'
                except ValueError:
                    self._logger.warning('Could not parse a datetime from '
                                         'lsstdoc date command: %r',
                                         command_content)

        # Fallback to getting the datetime from Git
        if doc_datetime is None:
            content_extensions = ('tex', 'bib', 'pdf', 'png', 'jpg')
            try:
                doc_datetime = get_content_commit_date(
                    content_extensions,
                    root_dir=self._root_dir)
                self._revision_datetime_source = 'git'
            except RuntimeError:
                self._logger.warning('Could not get a datetime from the Git '
                                     'repository at %r',
                                     self._root_dir)

        # Final fallback to the current datetime
        if doc_datetime is None:
            doc_datetime = pytz.utc.localize(datetime.datetime.now())
            self._revision_datetime_source = 'now'

        self._datetime = doc_datetime