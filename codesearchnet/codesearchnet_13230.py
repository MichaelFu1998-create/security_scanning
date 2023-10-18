def trim(self, start_time, end_time, strict=False):
        '''
        Trim the annotation and return as a new `Annotation` object.

        Trimming will result in the new annotation only containing observations
        that occur in the intersection of the time range spanned by the
        annotation and the time range specified by the user. The new annotation
        will span the time range ``[trim_start, trim_end]`` where
        ``trim_start = max(self.time, start_time)`` and ``trim_end =
        min(self.time + self.duration, end_time)``.

        If ``strict=False`` (default) observations that start before
        ``trim_start`` and end after it will be trimmed such that they start at
        ``trim_start``, and similarly observations that start before
        ``trim_end`` and end after it will be trimmed to end at ``trim_end``.
        If ``strict=True`` such borderline observations will be discarded.

        The new duration of the annotation will be ``trim_end - trim_start``.

        Note that if the range defined by ``[start_time, end_time]``
        doesn't intersect with the original time range spanned by the
        annotation the resulting annotation will contain no observations, will
        have the same start time as the original annotation and have duration
        0.

        This function also copies over all the annotation metadata from the
        original annotation and documents the trim operation by adding a list
        of tuples to the annotation's sandbox keyed by
        ``Annotation.sandbox.trim`` which documents each trim operation with a
        tuple ``(start_time, end_time, trim_start, trim_end)``.

        Parameters
        ----------
        start_time : float
            The desired start time for the trimmed annotation in seconds.
        end_time
            The desired end time for the trimmed annotation in seconds. Must be
            greater than ``start_time``.
        strict : bool
            When ``False`` (default) observations that lie at the boundaries of
            the trimming range (given by ``[trim_start, trim_end]`` as
            described above), i.e. observations that start before and end after
            either the trim start or end time, will have their time and/or
            duration adjusted such that only the part of the observation that
            lies within the trim range is kept. When ``True`` such observations
            are discarded and not included in the trimmed annotation.

        Returns
        -------
        ann_trimmed : Annotation
            The trimmed annotation, returned as a new jams.Annotation object.
            If the trim range specified by ``[start_time, end_time]`` does not
            intersect at all with the original time range of the annotation a
            warning will be issued and the returned annotation will be empty.

        Raises
        ------
        ParameterError
            If ``end_time`` is not greater than ``start_time``.

        Examples
        --------
        >>> ann = jams.Annotation(namespace='tag_open', time=2, duration=8)
        >>> ann.append(time=2, duration=2, value='one')
        >>> ann.append(time=4, duration=2, value='two')
        >>> ann.append(time=6, duration=2, value='three')
        >>> ann.append(time=7, duration=2, value='four')
        >>> ann.append(time=8, duration=2, value='five')
        >>> ann_trim = ann.trim(5, 8, strict=False)
        >>> print(ann_trim.time, ann_trim.duration)
        (5, 3)
        >>> ann_trim.to_dataframe()
           time  duration  value confidence
        0     5         1    two       None
        1     6         2  three       None
        2     7         1   four       None
        >>> ann_trim_strict = ann.trim(5, 8, strict=True)
        >>> print(ann_trim_strict.time, ann_trim_strict.duration)
        (5, 3)
        >>> ann_trim_strict.to_dataframe()
           time  duration  value confidence
        0     6         2  three       None
        '''
        # Check for basic start_time and end_time validity
        if end_time <= start_time:
            raise ParameterError(
                'end_time must be greater than start_time.')

        # If the annotation does not have a set duration value, we'll assume
        # trimming is possible (up to the user to ensure this is valid).
        if self.duration is None:
            orig_time = start_time
            orig_duration = end_time - start_time
            warnings.warn(
                "Annotation.duration is not defined, cannot check "
                "for temporal intersection, assuming the annotation "
                "is valid between start_time and end_time.")
        else:
            orig_time = self.time
            orig_duration = self.duration

        # Check whether there is intersection between the trim range and
        # annotation: if not raise a warning and set trim_start and trim_end
        # appropriately.
        if start_time > (orig_time + orig_duration) or (end_time < orig_time):
            warnings.warn(
                'Time range defined by [start_time,end_time] does not '
                'intersect with the time range spanned by this annotation, '
                'the trimmed annotation will be empty.')
            trim_start = self.time
            trim_end = trim_start
        else:
            # Determine new range
            trim_start = max(orig_time, start_time)
            trim_end = min(orig_time + orig_duration, end_time)

        # Create new annotation with same namespace/metadata
        ann_trimmed = Annotation(
            self.namespace,
            data=None,
            annotation_metadata=self.annotation_metadata,
            sandbox=self.sandbox,
            time=trim_start,
            duration=trim_end - trim_start)

        # Selectively add observations based on their start time / duration
        # We do this rather than copying and directly manipulating the
        # annotation' data frame (which might be faster) since this way trim is
        # independent of the internal data representation.
        for obs in self.data:

            obs_start = obs.time
            obs_end = obs_start + obs.duration

            if obs_start < trim_end and obs_end > trim_start:

                new_start = max(obs_start, trim_start)
                new_end = min(obs_end, trim_end)
                new_duration = new_end - new_start

                if ((not strict) or
                        (new_start == obs_start and new_end == obs_end)):
                    ann_trimmed.append(time=new_start,
                                       duration=new_duration,
                                       value=obs.value,
                                       confidence=obs.confidence)

        if 'trim' not in ann_trimmed.sandbox.keys():
            ann_trimmed.sandbox.update(
                trim=[{'start_time': start_time, 'end_time': end_time,
                       'trim_start': trim_start, 'trim_end': trim_end}])
        else:
            ann_trimmed.sandbox.trim.append(
                {'start_time': start_time, 'end_time': end_time,
                 'trim_start': trim_start, 'trim_end': trim_end})

        return ann_trimmed