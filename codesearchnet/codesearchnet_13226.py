def append(self, time=None, duration=None, value=None, confidence=None):
        '''Append an observation to the data field

        Parameters
        ----------
        time : float >= 0
        duration : float >= 0
            The time and duration of the new observation, in seconds
        value
        confidence
            The value and confidence of the new observations.

            Types and values should conform to the namespace of the
            Annotation object.

        Examples
        --------
        >>> ann = jams.Annotation(namespace='chord')
        >>> ann.append(time=3, duration=2, value='E#')
        '''

        self.data.add(Observation(time=float(time),
                                  duration=float(duration),
                                  value=value,
                                  confidence=confidence))