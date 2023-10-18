def slice(self, start_time, end_time, strict=False):
        '''
        Slice the annotation and return as a new `Annotation` object.

        Slicing has the same effect as trimming (see `Annotation.trim`) except
        that while trimming does not modify the start time of the annotation or
        the observations it contains, slicing will set the new annotation's
        start time to ``max(0, trimmed_annotation.time - start_time)`` and the
        start time of its observations will be set with respect to this new
        reference start time.

        This function documents the slice operation by adding a list of tuples
        to the annotation's sandbox keyed by ``Annotation.sandbox.slice`` which
        documents each slice operation with a tuple
        ``(start_time, end_time, slice_start, slice_end)``, where
        ``slice_start`` and ``slice_end`` are given by ``trim_start`` and
        ``trim_end`` (see `Annotation.trim`).

        Since slicing is implemented  using trimming, the trimming operation
        will also be documented in ``Annotation.sandbox.trim`` as described in
        `Annotation.trim`.

        This function is useful for example when trimming an audio file,
        allowing the user to trim the annotation while ensuring all time
        information matches the new trimmed audio file.

        Parameters
        ----------
        start_time : float
            The desired start time for slicing in seconds.
        end_time
            The desired end time for slicing in seconds. Must be greater than
            ``start_time``.
        strict : bool
            When ``False`` (default) observations that lie at the boundaries of
            the slice (see `Annotation.trim` for details) will have their time
            and/or duration adjusted such that only the part of the observation
            that lies within the slice range is kept. When ``True`` such
            observations are discarded and not included in the sliced
            annotation.

        Returns
        -------
        sliced_ann : Annotation
            The sliced annotation.

        See Also
        --------
        Annotation.trim

        Examples
        --------
        >>> ann = jams.Annotation(namespace='tag_open', time=2, duration=8)
        >>> ann.append(time=2, duration=2, value='one')
        >>> ann.append(time=4, duration=2, value='two')
        >>> ann.append(time=6, duration=2, value='three')
        >>> ann.append(time=7, duration=2, value='four')
        >>> ann.append(time=8, duration=2, value='five')
        >>> ann_slice = ann.slice(5, 8, strict=False)
        >>> print(ann_slice.time, ann_slice.duration)
        (0, 3)
        >>> ann_slice.to_dataframe()
           time  duration  value confidence
        0   0.0       1.0    two       None
        1   1.0       2.0  three       None
        2   2.0       1.0   four       None
        >>> ann_slice_strict = ann.slice(5, 8, strict=True)
        >>> print(ann_slice_strict.time, ann_slice_strict.duration)
        (0, 3)
        >>> ann_slice_strict.to_dataframe()
           time  duration  value confidence
        0   1.0       2.0  three       None
        '''
        # start by trimming the annotation
        sliced_ann = self.trim(start_time, end_time, strict=strict)
        raw_data = sliced_ann.pop_data()

        # now adjust the start time of the annotation and the observations it
        # contains.

        for obs in raw_data:
            new_time = max(0, obs.time - start_time)
            # if obs.time > start_time,
            #   duration doesn't change
            # if obs.time < start_time,
            #   duration shrinks by start_time - obs.time
            sliced_ann.append(time=new_time,
                              duration=obs.duration,
                              value=obs.value,
                              confidence=obs.confidence)

        ref_time = sliced_ann.time
        slice_start = ref_time
        slice_end = ref_time + sliced_ann.duration

        if 'slice' not in sliced_ann.sandbox.keys():
            sliced_ann.sandbox.update(
                slice=[{'start_time': start_time, 'end_time': end_time,
                        'slice_start': slice_start, 'slice_end': slice_end}])
        else:
            sliced_ann.sandbox.slice.append(
                {'start_time': start_time, 'end_time': end_time,
                 'slice_start': slice_start, 'slice_end': slice_end})

        # Update the timing for the sliced annotation
        sliced_ann.time = max(0, ref_time - start_time)

        return sliced_ann