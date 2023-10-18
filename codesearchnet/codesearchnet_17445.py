def imagecapture(self, window_name=None, out_file=None, x=0, y=0,
                     width=None, height=None):
        """
        Captures screenshot of the whole desktop or given window

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param x: x co-ordinate value
        @type x: integer
        @param y: y co-ordinate value
        @type y: integer
        @param width: width co-ordinate value
        @type width: integer
        @param height: height co-ordinate value
        @type height: integer

        @return: screenshot filename
        @rtype: string
        """
        if not out_file:
            out_file = tempfile.mktemp('.png', 'ldtp_')
        else:
            out_file = os.path.expanduser(out_file)

        ### Windows compatibility
        if _ldtp_windows_env:
            if width == None:
                width = -1
            if height == None:
                height = -1
            if window_name == None:
                window_name = ''
        ### Windows compatibility - End
        data = self._remote_imagecapture(window_name, x, y, width, height)
        f = open(out_file, 'wb')
        f.write(b64decode(data))
        f.close()
        return out_file