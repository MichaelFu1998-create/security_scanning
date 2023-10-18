def end_write(self, with_errors):
        """Called when PUT has finished writing.

        See DAVResource.end_write()
        """
        if not with_errors:
            commands.add(self.provider.ui, self.provider.repo, self.localHgPath)