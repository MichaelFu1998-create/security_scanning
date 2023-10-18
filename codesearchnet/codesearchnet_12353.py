def child_added(self, child):
        """ If a child is added we have to make sure the map adapter exists """
        if child.widget:
            # TODO: Should we keep count and remove the adapter if not all
            # markers request it?
            self.parent().init_info_window_adapter()
        super(AndroidMapMarker, self).child_added(child)