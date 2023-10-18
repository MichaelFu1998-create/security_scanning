def on_marker(self, mid):
        """ Convert our options into the actual circle object"""
        self.marker = Circle(__id__=mid)
        self.parent().markers[mid] = self

        #: Required so the packer can pass the id
        self.marker.setTag(mid)

        d = self.declaration
        if d.clickable:
            self.set_clickable(d.clickable)

        #: Can free the options now
        del self.options