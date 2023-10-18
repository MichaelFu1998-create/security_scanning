def slice(self, start_time, end_time, strict=False):
        '''
        Slice every annotation contained in the annotation array using
        `Annotation.slice`
        and return as a new AnnotationArray

        See `Annotation.slice` for details about slicing. This function does
        not modify the annotations in the original annotation array.

        Parameters
        ----------
        start_time : float
            The desired start time for slicing in seconds.
        end_time
            The desired end time for slicing in seconds. Must be greater than
            ``start_time``.
        strict : bool
            When ``False`` (default) observations that lie at the boundaries of
            the slicing range (see `Annotation.slice` for details) will have
            their time and/or duration adjusted such that only the part of the
            observation that lies within the trim range is kept. When ``True``
            such observations are discarded and not included in the sliced
            annotation.

        Returns
        -------
        sliced_array : AnnotationArray
            An annotation array where every annotation has been sliced.
        '''
        sliced_array = AnnotationArray()
        for ann in self:
            sliced_array.append(ann.slice(start_time, end_time, strict=strict))

        return sliced_array