def _transform(self, jam, state):
        '''Apply the transformation to audio and annotations.

        The input jam is copied and modified, and returned
        contained in a list.

        Parameters
        ----------
        jam : jams.JAMS
            A single jam object to modify

        Returns
        -------
        jam_list : list
            A length-1 list containing `jam` after transformation

        See also
        --------
        core.load_jam_audio
        '''

        if not hasattr(jam.sandbox, 'muda'):
            raise RuntimeError('No muda state found in jams sandbox.')

        # We'll need a working copy of this object for modification purposes
        jam_w = copy.deepcopy(jam)

        # Push our reconstructor onto the history stack
        jam_w.sandbox.muda['history'].append({'transformer': self.__serialize__,
                                              'state': state})

        if hasattr(self, 'audio'):
            self.audio(jam_w.sandbox.muda, state)

        if hasattr(self, 'metadata'):
            self.metadata(jam_w.file_metadata, state)

        # Walk over the list of deformers
        for query, function_name in six.iteritems(self.dispatch):
            function = getattr(self, function_name)
            for matched_annotation in jam_w.search(namespace=query):
                function(matched_annotation, state)

        return jam_w