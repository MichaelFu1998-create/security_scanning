def destroy(self):
        """ Remove the marker if it was added to the map when destroying"""
        marker = self.marker
        parent = self.parent()
        if marker:
            if parent:
                del parent.markers[marker.__id__]
            marker.remove()
        super(AndroidMapItemBase, self).destroy()