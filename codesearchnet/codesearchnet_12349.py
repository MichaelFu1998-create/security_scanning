def on_map_fragment_created(self, obj_id):
        """ Create the fragment and pull the map reference when it's loaded. 
        """
        self.fragment = MapFragment(__id__=obj_id)

        #: Setup callback so we know when the map is ready
        self.map.onMapReady.connect(self.on_map_ready)
        self.fragment.getMapAsync(self.map.getId())

        context = self.get_context()

        def on_transaction(id):
            trans = FragmentTransaction(__id__=id)
            trans.add(self.widget.getId(), self.fragment)
            trans.commit()

        def on_fragment_manager(id):
            fm = FragmentManager(__id__=id)
            fm.beginTransaction().then(on_transaction)

        context.widget.getSupportFragmentManager().then(on_fragment_manager)