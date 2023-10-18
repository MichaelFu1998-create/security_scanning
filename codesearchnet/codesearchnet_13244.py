def trim(self, start_time, end_time, strict=False):
        '''
        Trim all the annotations inside the jam and return as a new `JAMS`
        object.

        See `Annotation.trim` for details about how the annotations
        are trimmed.

        This operation is also documented in the jam-level sandbox
        with a list keyed by ``JAMS.sandbox.trim`` containing a tuple for each
        jam-level trim of the form ``(start_time, end_time)``.

        This function also copies over all of the file metadata from the
        original jam.

        Note: trimming does not affect the duration of the jam, i.e. the value
        of ``JAMS.file_metadata.duration`` will be the same for the original
        and trimmed jams.

        Parameters
        ----------
        start_time : float
            The desired start time for the trimmed annotations in seconds.
        end_time
            The desired end time for trimmed annotations in seconds. Must be
            greater than ``start_time``.
        strict : bool
            When ``False`` (default) observations that lie at the boundaries of
            the trimming range (see `Annotation.trim` for details), will have
            their time and/or duration adjusted such that only the part of the
            observation that lies within the trim range is kept. When ``True``
            such observations are discarded and not included in the trimmed
            annotation.

        Returns
        -------
        jam_trimmed : JAMS
            The trimmed jam with trimmed annotations, returned as a new JAMS
            object.

        '''
        # Make sure duration is set in file metadata
        if self.file_metadata.duration is None:
            raise JamsError(
                'Duration must be set (jam.file_metadata.duration) before '
                'trimming can be performed.')

        # Make sure start and end times are within the file start/end times
        if not (0 <= start_time <= end_time <= float(
                self.file_metadata.duration)):
            raise ParameterError(
                'start_time and end_time must be within the original file '
                'duration ({:f}) and end_time cannot be smaller than '
                'start_time.'.format(float(self.file_metadata.duration)))

        # Create a new jams
        jam_trimmed = JAMS(annotations=None,
                           file_metadata=self.file_metadata,
                           sandbox=self.sandbox)

        # trim annotations
        jam_trimmed.annotations = self.annotations.trim(
            start_time, end_time, strict=strict)

        # Document jam-level trim in top level sandbox
        if 'trim' not in jam_trimmed.sandbox.keys():
            jam_trimmed.sandbox.update(
                trim=[{'start_time': start_time, 'end_time': end_time}])
        else:
            jam_trimmed.sandbox.trim.append(
                {'start_time': start_time, 'end_time': end_time})

        return jam_trimmed