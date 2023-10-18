def clearContents(cls):
        """Clear contents of general pasteboard.

        Future enhancement can include specifying which clipboard to clear
        Returns: True on success; caller should expect to catch exceptions,
                 probably from AppKit (ValueError)
        """
        log_msg = 'Request to clear contents of pasteboard: general'
        logging.debug(log_msg)
        pb = AppKit.NSPasteboard.generalPasteboard()
        pb.clearContents()
        return True