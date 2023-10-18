def _verify(self, payload):
        """
        ensure that all files to be attached exist
        open()'s better than exists(), cos it avoids a race condition
        """
        if not payload:  # Check payload has nonzero length
            raise ze.ParamNotPassed
        for templt in payload:
            if os.path.isfile(str(self.basedir.joinpath(templt["filename"]))):
                try:
                    # if it is a file, try to open it, and catch the error
                    with open(str(self.basedir.joinpath(templt["filename"]))):
                        pass
                except IOError:
                    raise ze.FileDoesNotExist(
                        "The file at %s couldn't be opened or found."
                        % str(self.basedir.joinpath(templt["filename"]))
                    )
            # no point in continuing if the file isn't a file
            else:
                raise ze.FileDoesNotExist(
                    "The file at %s couldn't be opened or found."
                    % str(self.basedir.joinpath(templt["filename"]))
                )