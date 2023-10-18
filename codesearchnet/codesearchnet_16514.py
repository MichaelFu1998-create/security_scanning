def parse(self,DXfield):
        """Parse the dx file and construct a DX field object with component classes.

        A :class:`field` instance *DXfield* must be provided to be
        filled by the parser::

           DXfield_object = OpenDX.field(*args)
           parse(DXfield_object)

        A tokenizer turns the dx file into a stream of tokens. A
        hierarchy of parsers examines the stream. The level-0 parser
        ('general') distinguishes comments and objects (level-1). The
        object parser calls level-3 parsers depending on the object
        found. The basic idea is that of a 'state machine'. There is
        one parser active at any time. The main loop is the general
        parser.

        * Constructing the dx objects with classtype and classid is
          not implemented yet.
        * Unknown tokens raise an exception.
        """

        self.DXfield = DXfield              # OpenDX.field (used by comment parser)
        self.currentobject = None           # containers for data
        self.objects = []                   # |
        self.tokens = []                    # token buffer
        with open(self.filename,'r') as self.dxfile:
            self.use_parser('general')      # parse the whole file and populate self.objects

        # assemble field from objects
        for o in self.objects:
            if o.type == 'field':
                # Almost ignore the field object; VMD, for instance,
                # does not write components. To make this work
                # seamlessly I have to think harder how to organize
                # and use the data, eg preping the field object
                # properly and the initializing. Probably should also
                # check uniqueness of ids etc.
                DXfield.id = o.id
                continue
            c = o.initialize()
            self.DXfield.add(c.component,c)

        # free space
        del self.currentobject, self.objects