def write(self, filename):
        """Write the complete dx object to the file.

        This is the simple OpenDX format which includes the data into
        the header via the 'object array ... data follows' statement.

        Only simple regular arrays are supported.

        The format should be compatible with VMD's dx reader plugin.
        """
        # comments (VMD chokes on lines of len > 80, so truncate)
        maxcol = 80
        with open(filename,'w') as outfile:
            for line in self.comments:
                comment = '# '+str(line)
                outfile.write(comment[:maxcol]+'\n')
            # each individual object
            for component,object in self.sorted_components():
                object.write(outfile)
            # the field object itself
            DXclass.write(self,outfile,quote=True)
            for component,object in self.sorted_components():
                outfile.write('component "%s" value %s\n' % (component,str(object.id)))