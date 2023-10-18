def trim(self, start_time, end_time, strict=False):
        '''
        Trim every annotation contained in the annotation array using
        `Annotation.trim` and return as a new `AnnotationArray`.

        See `Annotation.trim` for details about trimming. This function does
        not modify the annotations in the original annotation array.


        Parameters
        ----------
        start_time : float
            The desired start time for the trimmed annotations in seconds.
        end_time
            The desired end time for trimmed annotations in seconds. Must be
            greater than ``start_time``.
        strict : bool
            When ``False`` (default) observations that lie at the boundaries of
            the trimming range (see `Annotation.trim` for details) will have
            their time and/or duration adjusted such that only the part of the
            observation that lies within the trim range is kept. When ``True``
            such observations are discarded and not included in the trimmed
            annotation.

        Returns
        -------
        trimmed_array : AnnotationArray
            An annotation array where every annotation has been trimmed.
        '''
        trimmed_array = AnnotationArray()
        for ann in self:
            trimmed_array.append(ann.trim(start_time, end_time, strict=strict))

        return trimmed_array