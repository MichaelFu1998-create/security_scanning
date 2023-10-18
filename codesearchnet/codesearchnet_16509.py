def read(self,file):
        """Read DX field from file.

            dx = OpenDX.field.read(dxfile)

        The classid is discarded and replaced with the one from the file.
        """
        DXfield = self
        p = DXParser(file)
        p.parse(DXfield)