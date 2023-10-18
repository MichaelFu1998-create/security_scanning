def __get_live_version(self):
        """
        Get a live version string using versiontools
        """
        try:
            import versiontools
        except ImportError:
            return None
        else:
            return str(versiontools.Version.from_expression(self.name))