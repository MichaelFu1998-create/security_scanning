def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        if change['type'] == 'container':
            #: Only update what's needed
            self.proxy.update_points(change)
        else:
            super(MapPolyline, self)._update_proxy(change)