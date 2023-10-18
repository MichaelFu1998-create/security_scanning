def init_info_window_adapter(self):
        """ Initialize the info window adapter. Should only be done if one of 
        the markers defines a custom view.
        """
        adapter = self.adapter
        if adapter:
            return  #: Already initialized
        adapter = GoogleMap.InfoWindowAdapter()
        adapter.getInfoContents.connect(self.on_info_window_contents_requested)
        adapter.getInfoWindow.connect(self.on_info_window_requested)
        self.map.setInfoWindowAdapter(adapter)