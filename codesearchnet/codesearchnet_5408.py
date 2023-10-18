def _inherit_data(self):
        """
        Inherits the data from the parent.
        """
        LOG.debug("'%s' inheriting data from '%s'" % (self.get_name(),
                                                      self.parent.get_name()),
                  extra=dict(data=self.parent.data))
        self.set_data(**self.parent.data)