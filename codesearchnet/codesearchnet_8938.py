def render(self, files=True):
        """
        Converts the configuration dictionary into the corresponding configuration format

        :param files: whether to include "additional files" in the output or not;
                      defaults to ``True``
        :returns: string with output
        """
        self.validate()
        # convert NetJSON config to intermediate data structure
        if self.intermediate_data is None:
            self.to_intermediate()
        # support multiple renderers
        renderers = getattr(self, 'renderers', None) or [self.renderer]
        # convert intermediate data structure to native configuration
        output = ''
        for renderer_class in renderers:
            renderer = renderer_class(self)
            output += renderer.render()
            # remove reference to renderer instance (not needed anymore)
            del renderer
        # are we required to include
        # additional files?
        if files:
            # render additional files
            files_output = self._render_files()
            if files_output:
                # max 2 new lines
                output += files_output.replace('\n\n\n', '\n\n')
        # return the configuration
        return output