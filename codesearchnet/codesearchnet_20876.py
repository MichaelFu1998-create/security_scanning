def load_attachments(self, source, skeleton):
        '''Load attachment configuration from the given text source.

        The attachment configuration file has a simple format. After discarding
        Unix-style comments (any part of a line that starts with the pound (#)
        character), each line in the file is then expected to have the following
        format::

            marker-name body-name X Y Z

        The marker name must correspond to an existing "channel" in our marker
        data. The body name must correspond to a rigid body in the skeleton. The
        X, Y, and Z coordinates specify the body-relative offsets where the
        marker should be attached: 0 corresponds to the center of the body along
        the given axis, while -1 and 1 correspond to the minimal (maximal,
        respectively) extent of the body's bounding box along the corresponding
        dimension.

        Parameters
        ----------
        source : str or file-like
            A filename or file-like object that we can use to obtain text
            configuration that describes how markers are attached to skeleton
            bodies.

        skeleton : :class:`pagoda.skeleton.Skeleton`
            The skeleton to attach our marker data to.
        '''
        self.targets = {}
        self.offsets = {}

        filename = source
        if isinstance(source, str):
            source = open(source)
        else:
            filename = '(file-{})'.format(id(source))

        for i, line in enumerate(source):
            tokens = line.split('#')[0].strip().split()
            if not tokens:
                continue
            label = tokens.pop(0)
            if label not in self.channels:
                logging.info('%s:%d: unknown marker %s', filename, i, label)
                continue
            if not tokens:
                continue
            name = tokens.pop(0)
            bodies = [b for b in skeleton.bodies if b.name == name]
            if len(bodies) != 1:
                logging.info('%s:%d: %d skeleton bodies match %s',
                             filename, i, len(bodies), name)
                continue
            b = self.targets[label] = bodies[0]
            o = self.offsets[label] = \
                np.array(list(map(float, tokens))) * b.dimensions / 2
            logging.info('%s <--> %s, offset %s', label, b.name, o)