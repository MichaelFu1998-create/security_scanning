def _export_dx(self, filename, type=None, typequote='"', **kwargs):
        """Export the density grid to an OpenDX file.

        The file format is the simplest regular grid array and it is
        also understood by VMD's and Chimera's DX reader; PyMOL
        requires the dx `type` to be set to "double".

        For the file format see
        http://opendx.sdsc.edu/docs/html/pages/usrgu068.htm#HDREDF

        """
        root, ext = os.path.splitext(filename)
        filename = root + '.dx'

        comments = [
            'OpenDX density file written by gridDataFormats.Grid.export()',
            'File format: http://opendx.sdsc.edu/docs/html/pages/usrgu068.htm#HDREDF',
            'Data are embedded in the header and tied to the grid positions.',
            'Data is written in C array order: In grid[x,y,z] the axis z is fastest',
            'varying, then y, then finally x, i.e. z is the innermost loop.'
        ]

        # write metadata in comments section
        if self.metadata:
            comments.append('Meta data stored with the python Grid object:')
        for k in self.metadata:
            comments.append('   ' + str(k) + ' = ' + str(self.metadata[k]))
        comments.append(
            '(Note: the VMD dx-reader chokes on comments below this line)')

        components = dict(
            positions=OpenDX.gridpositions(1, self.grid.shape, self.origin,
                                           self.delta),
            connections=OpenDX.gridconnections(2, self.grid.shape),
            data=OpenDX.array(3, self.grid, type=type, typequote=typequote),
        )
        dx = OpenDX.field('density', components=components, comments=comments)
        dx.write(filename)