def isEmpty(cls, datatype=None):
        """Method to test if the general pasteboard is empty or not with respect
        to the type of object you want.

        Parameters: datatype (defaults to strings)
        Returns: Boolean True (empty) / False (has contents); Raises
                 exception (passes any raised up)
        """
        if not datatype:
            datatype = AppKit.NSString
        if not isinstance(datatype, types.ListType):
            datatype = [datatype]
        pp = pprint.PrettyPrinter()
        logging.debug('Desired datatypes: %s' % pp.pformat(datatype))
        opt_dict = {}
        logging.debug('Results filter is: %s' % pp.pformat(opt_dict))

        try:
            log_msg = 'Request to verify pasteboard is empty'
            logging.debug(log_msg)
            pb = AppKit.NSPasteboard.generalPasteboard()
            # canReadObjectForClasses_options_() seems to return an int (> 0 if
            # True)
            # Need to negate to get the sense we want (True if can not read the
            # data type from the pasteboard)
            its_empty = not bool(pb.canReadObjectForClasses_options_(datatype,
                                                                     opt_dict))
        except ValueError as error:
            logging.error(error)
            raise

        return bool(its_empty)