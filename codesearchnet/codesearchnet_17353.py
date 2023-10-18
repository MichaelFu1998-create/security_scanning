def paste(cls):
        """Get the clipboard data ('Paste').

        Returns: Data (string) retrieved or None if empty. Exceptions from
        AppKit will be handled by caller.
        """
        pb = AppKit.NSPasteboard.generalPasteboard()

        # If we allow for multiple data types (e.g. a list of data types)
        # we will have to add a condition to check just the first in the
        # list of datatypes)
        data = pb.stringForType_(cls.STRING)
        return data