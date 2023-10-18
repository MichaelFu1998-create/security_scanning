def media(self):
        """Media defined as a dynamic property instead of an inner class."""
        media = super(ChainedSelectMultiple, self).media
        js = ['smart-selects/admin/js/chainedm2m.js',
              'smart-selects/admin/js/bindfields.js']
        if self.horizontal:
            # For horizontal mode add django filter horizontal javascript code
            js.extend(["admin/js/core.js",
                       "admin/js/SelectBox.js",
                       "admin/js/SelectFilter2.js"])
        media += Media(js=js)
        return media