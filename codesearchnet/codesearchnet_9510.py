def grab_to_file(self, filename, bbox=None):
        """http://www.pygtk.org/docs/pygtk/class-gdkpixbuf.html.

        only "jpeg" or "png"
        """

        w = self.gtk.gdk.get_default_root_window()
#       Capture the whole screen.
        if bbox is None:
            sz = w.get_size()
            pb = self.gtk.gdk.Pixbuf(
                self.gtk.gdk.COLORSPACE_RGB, False, 8, sz[0], sz[1])  # 24bit RGB
            pb = pb.get_from_drawable(
                w, w.get_colormap(), 0, 0, 0, 0, sz[0], sz[1])
#       Only capture what we need. The smaller the capture, the faster.
        else:
            sz = [bbox[2] - bbox[0], bbox[3] - bbox[1]]
            pb = self.gtk.gdk.Pixbuf(
                self.gtk.gdk.COLORSPACE_RGB, False, 8, sz[0], sz[1])
            pb = pb.get_from_drawable(
                w, w.get_colormap(), bbox[0], bbox[1], 0, 0, sz[0], sz[1])
        assert pb
        ftype = 'png'
        if filename.endswith('.jpeg'):
            ftype = 'jpeg'

        pb.save(filename, ftype)