def process_macros(self, content: str) -> str:
        '''Replace macros with content defined in the config.

        :param content: Markdown content

        :returns: Markdown content without macros
        '''

        def _sub(macro):
            name = macro.group('body')
            params = self.get_options(macro.group('options'))

            return self.options['macros'].get(name, '').format_map(params)

        return self.pattern.sub(_sub, content)