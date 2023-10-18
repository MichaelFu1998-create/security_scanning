def stitch_coordinates(self, well_row=0, well_column=0):
        """Get a list of stitch coordinates for the given well.

        Parameters
        ----------
        well_row : int
            Y well coordinate. Same as --V in files.
        well_column : int
            X well coordinate. Same as --U in files.

        Returns
        -------
        (xs, ys, attr) : tuples with float and collections.OrderedDict
            Tuple of x's, y's and attributes.
        """
        well = [w for w in self.wells
                    if attribute(w, 'u') == well_column and
                       attribute(w, 'v') == well_row]

        if len(well) == 1:
            well = well[0]
            tile = os.path.join(well, 'TileConfiguration.registered.txt')

            with open(tile) as f:
                data = [x.strip()
                            for l in f.readlines()
                                if l[0:7] == 'image--'
                                    for x in l.split(';')] # flat list
                coordinates = (ast.literal_eval(x) for x in data[2::3])
                # flatten
                coordinates = sum(coordinates, ())
                attr = tuple(attributes(x) for x in data[0::3])
            return coordinates[0::2], coordinates[1::2], attr

        else:
            print('leicaexperiment stitch_coordinates'
                  '({}, {}) Well not found'.format(well_row, well_column))