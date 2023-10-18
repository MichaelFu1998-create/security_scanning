def add_context(self, err_context, succ_context=None):
    """ Prepend msg to add some context information

    :param pmsg: context info
    :return: None
    """
    self.err_context = err_context
    self.succ_context = succ_context