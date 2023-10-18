def grab(self, bbox=None):
        """Grabs an image directly to a buffer.

        :param bbox: Optional tuple or list containing (x1, y1, x2, y2) coordinates
            of sub-region to capture.
        :return: PIL RGB image
        :raises: ValueError, if image data does not have 3 channels (RGB), each with 8
            bits.
        :rtype: Image
        """
        w = Gdk.get_default_root_window()
        if bbox is not None:
            g = [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]
        else:
            g = w.get_geometry()
        pb = Gdk.pixbuf_get_from_window(w, *g)
        if pb.get_bits_per_sample() != 8:
            raise ValueError('Expected 8 bits per pixel.')
        elif pb.get_n_channels() != 3:
            raise ValueError('Expected RGB image.')

        # Read the entire buffer into a python bytes object.
        # read_pixel_bytes: New in version 2.32.
        pixel_bytes = pb.read_pixel_bytes().get_data()  # type: bytes
        width, height = g[2], g[3]

        # Probably for SSE alignment reasons, the pixbuf has extra data in each line.
        # The args after "raw" help handle this; see
        # http://effbot.org/imagingbook/decoder.htm#the-raw-decoder
        return Image.frombytes(
            'RGB', (width, height), pixel_bytes, 'raw', 'RGB', pb.get_rowstride(), 1)