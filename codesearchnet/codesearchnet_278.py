def clip_out_of_image(self, image):
        """
        Clip off all parts of the line_string that are outside of the image.

        Parameters
        ----------
        image : ndarray or tuple of int
            Either an image with shape ``(H,W,[C])`` or a tuple denoting
            such an image shape.

        Returns
        -------
        list of imgaug.augmentables.lines.LineString
            Line strings, clipped to the image shape.
            The result may contain any number of line strins, including zero.

        """
        if len(self.coords) == 0:
            return []

        inside_image_mask = self.get_pointwise_inside_image_mask(image)
        ooi_mask = ~inside_image_mask

        if len(self.coords) == 1:
            if not np.any(inside_image_mask):
                return []
            return [self.copy()]

        if np.all(inside_image_mask):
            return [self.copy()]

        # top, right, bottom, left image edges
        # we subtract eps here, because intersection() works inclusively,
        # i.e. not subtracting eps would be equivalent to 0<=x<=C for C being
        # height or width
        # don't set the eps too low, otherwise points at height/width seem
        # to get rounded to height/width by shapely, which can cause problems
        # when first clipping and then calling is_fully_within_image()
        # returning false
        height, width = normalize_shape(image)[0:2]
        eps = 1e-3
        edges = [
            LineString([(0.0, 0.0), (width - eps, 0.0)]),
            LineString([(width - eps, 0.0), (width - eps, height - eps)]),
            LineString([(width - eps, height - eps), (0.0, height - eps)]),
            LineString([(0.0, height - eps), (0.0, 0.0)])
        ]
        intersections = self.find_intersections_with(edges)

        points = []
        gen = enumerate(zip(self.coords[:-1], self.coords[1:],
                            ooi_mask[:-1], ooi_mask[1:],
                            intersections))
        for i, (line_start, line_end, ooi_start, ooi_end, inter_line) in gen:
            points.append((line_start, False, ooi_start))
            for p_inter in inter_line:
                points.append((p_inter, True, False))

            is_last = (i == len(self.coords) - 2)
            if is_last and not ooi_end:
                points.append((line_end, False, ooi_end))

        lines = []
        line = []
        for i, (coord, was_added, ooi) in enumerate(points):
            # remove any point that is outside of the image,
            # also start a new line once such a point is detected
            if ooi:
                if len(line) > 0:
                    lines.append(line)
                    line = []
                continue

            if not was_added:
                # add all points that were part of the original line string
                # AND that are inside the image plane
                line.append(coord)
            else:
                is_last_point = (i == len(points)-1)
                # ooi is a numpy.bool_, hence the bool(.)
                is_next_ooi = (not is_last_point
                               and bool(points[i+1][2]) is True)

                # Add all points that were new (i.e. intersections), so
                # long that they aren't essentially identical to other point.
                # This prevents adding overlapping intersections multiple times.
                # (E.g. when a line intersects with a corner of the image plane
                # and also with one of its edges.)
                p_prev = line[-1] if len(line) > 0 else None
                # ignore next point if end reached or next point is out of image
                p_next = None
                if not is_last_point and not is_next_ooi:
                    p_next = points[i+1][0]
                dist_prev = None
                dist_next = None
                if p_prev is not None:
                    dist_prev = np.linalg.norm(
                        np.float32(coord) - np.float32(p_prev))
                if p_next is not None:
                    dist_next = np.linalg.norm(
                        np.float32(coord) - np.float32(p_next))

                dist_prev_ok = (dist_prev is None or dist_prev > 1e-2)
                dist_next_ok = (dist_next is None or dist_next > 1e-2)
                if dist_prev_ok and dist_next_ok:
                    line.append(coord)

        if len(line) > 0:
            lines.append(line)

        lines = [line for line in lines if len(line) > 0]
        return [self.deepcopy(coords=line) for line in lines]