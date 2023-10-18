def media(self):
        """Media defined as a dynamic property instead of an inner class."""
        media = super(ChainedSelect, self).media
        js = ['smart-selects/admin/js/chainedfk.js',
              'smart-selects/admin/js/bindfields.js']
        media += Media(js=js)
        return media