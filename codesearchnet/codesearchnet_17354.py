def copy(cls, data):
        """Set the clipboard data ('Copy').

        Parameters: data to set (string)
        Optional: datatype if it's not a string
        Returns: True / False on successful copy, Any exception raised (like
                 passes the NSPasteboardCommunicationError) should be caught
                 by the caller.
        """
        pp = pprint.PrettyPrinter()

        copy_data = 'Data to copy (put in pasteboard): %s'
        logging.debug(copy_data % pp.pformat(data))

        # Clear the pasteboard first:
        cleared = cls.clearAll()
        if not cleared:
            logging.warning('Clipboard could not clear properly')
            return False

        # Prepare to write the data
        # If we just use writeObjects the sequence to write to the clipboard is
        # a) Call clearContents()
        # b) Call writeObjects() with a list of objects to write to the
        #    clipboard
        if not isinstance(data, types.ListType):
            data = [data]

        pb = AppKit.NSPasteboard.generalPasteboard()
        pb_set_ok = pb.writeObjects_(data)

        return bool(pb_set_ok)