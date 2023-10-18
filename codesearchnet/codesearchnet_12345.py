def create_widget(self):
        """ Create the underlying widget.

        """
        self.init_options()

        #: Retrieve the actual map
        MapFragment.newInstance(self.options).then(
            self.on_map_fragment_created)

        # Holder for the fragment
        self.widget = FrameLayout(self.get_context())

        # I wrote this a few days ago and already forget how this hack works...
        # lol We can't simply get a map reference using getMapAsync in the
        # return value like we normally do with a normal call function return
        # value. The bridge design was modified to store an object that cannot
        # be decoded normally (via a standard Bridge.Packer) by saving the new
        # object in the cache returning the id of the handler or proxy that
        # invoked it. This way we can manually create a new id and pass that
        # "future reference-able" object as our listener. At which point the
        # bridge will create a reference entry in the cache for us with the of
        # the object we gave it. Once in the cache we can use it like any
        # bridge object we created.
        self.map = GoogleMap(__id__=bridge.generate_id())