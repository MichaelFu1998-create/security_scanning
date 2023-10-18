def on_marker(self, marker):
        """ Convert our options into the actual marker object"""
        mid, pos = marker
        self.marker = Marker(__id__=mid)
        mapview = self.parent()
        # Save ref
        mapview.markers[mid] = self

        # Required so the packer can pass the id
        self.marker.setTag(mid)

        # If we have a child widget we must configure the map to use the
        # custom adapter
        for w in self.child_widgets():
            mapview.init_info_window_adapter()
            break

        d = self.declaration
        if d.show_info:
            self.set_show_info(d.show_info)

        #: Can free the options now
        del self.options