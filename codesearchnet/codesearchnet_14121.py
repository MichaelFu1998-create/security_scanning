def _locate(self, t, segments=None):
        """ Locates t on a specific segment in the path.
            Returns (index, t, PathElement)
            A path is a combination of lines and curves (segments).
            The returned index indicates the start of the segment that contains point t.
            The returned t is the absolute time on that segment,
            in contrast to the relative t on the whole of the path.
            The returned point is the last MOVETO, any subsequent CLOSETO after i closes to that point.
            When you supply the list of segment lengths yourself, as returned from length(path, segmented=True),
            point() works about thirty times faster in a for-loop since it doesn't need to recalculate
            the length during each iteration.
        """
        # Originally from nodebox-gl
        if segments is None:
            segments = self._segment_lengths(relative=True)
        if len(segments) == 0:
            raise PathError, "The given path is empty"
        for i, el in enumerate(self._get_elements()):
            if i == 0 or el.cmd == MOVETO:
                closeto = Point(el.x, el.y)
            if t <= segments[i] or i == len(segments) - 1:
                break
            else:
                t -= segments[i]
        try:
            t /= segments[i]
        except ZeroDivisionError:
            pass
        if i == len(segments) - 1 and segments[i] == 0:
            i -= 1
        return (i, t, closeto)