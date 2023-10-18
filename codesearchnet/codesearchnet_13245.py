def slice(self, start_time, end_time, strict=False):
        '''
        Slice all the annotations inside the jam and return as a new `JAMS`
        object.

        See `Annotation.slice` for details about how the annotations
        are sliced.

        This operation is also documented in the jam-level sandbox
        with a list keyed by ``JAMS.sandbox.slice`` containing a tuple for each
        jam-level slice of the form ``(start_time, end_time)``.

        Since slicing is implemented using trimming, the operation will also be
        documented in ``JAMS.sandbox.trim`` as described in `JAMS.trim`.

        This function also copies over all of the file metadata from the
        original jam.

        Note: slicing will affect the duration of the jam, i.e. the new value
        of ``JAMS.file_metadata.duration`` will be ``end_time - start_time``.

        Parameters
        ----------
        start_time : float
            The desired start time for slicing in seconds.
        end_time
            The desired end time for slicing in seconds. Must be greater than
            ``start_time``.
        strict : bool
            When ``False`` (default) observations that lie at the boundaries of
            the slicing range (see `Annotation.slice` for details), will have
            their time and/or duration adjusted such that only the part of the
            observation that lies within the slice range is kept. When ``True``
            such observations are discarded and not included in the sliced
            annotation.

        Returns
        -------
        jam_sliced: JAMS
            The sliced jam with sliced annotations, returned as a new
            JAMS object.

        '''
        # Make sure duration is set in file metadata
        if self.file_metadata.duration is None:
            raise JamsError(
                'Duration must be set (jam.file_metadata.duration) before '
                'slicing can be performed.')

        # Make sure start and end times are within the file start/end times
        if (start_time < 0 or
                start_time > float(self.file_metadata.duration) or
                end_time < start_time or
                end_time > float(self.file_metadata.duration)):
            raise ParameterError(
                'start_time and end_time must be within the original file '
                'duration ({:f}) and end_time cannot be smaller than '
                'start_time.'.format(float(self.file_metadata.duration)))

        # Create a new jams
        jam_sliced = JAMS(annotations=None,
                          file_metadata=self.file_metadata,
                          sandbox=self.sandbox)

        # trim annotations
        jam_sliced.annotations = self.annotations.slice(
            start_time, end_time, strict=strict)

        # adjust dutation
        jam_sliced.file_metadata.duration = end_time - start_time

        # Document jam-level trim in top level sandbox
        if 'slice' not in jam_sliced.sandbox.keys():
            jam_sliced.sandbox.update(
                slice=[{'start_time': start_time, 'end_time': end_time}])
        else:
            jam_sliced.sandbox.slice.append(
                {'start_time': start_time, 'end_time': end_time})

        return jam_sliced