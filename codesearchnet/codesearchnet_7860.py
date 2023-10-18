def remix(self, remix_dictionary=None, num_output_channels=None):
        '''Remix the channels of an audio file.

        Note: volume options are not yet implemented

        Parameters
        ----------
        remix_dictionary : dict or None
            Dictionary mapping output channel to list of input channel(s).
            Empty lists indicate the corresponding output channel should be
            empty. If None, mixes all channels down to a single mono file.
        num_output_channels : int or None
            The number of channels in the output file. If None, the number of
            output channels is equal to the largest key in remix_dictionary.
            If remix_dictionary is None, this variable is ignored.

        Examples
        --------
        Remix a 4-channel input file. The output file will have
        input channel 2 in channel 1, a mixdown of input channels 1 an 3 in
        channel 2, an empty channel 3, and a copy of input channel 4 in
        channel 4.

        >>> import sox
        >>> tfm = sox.Transformer()
        >>> remix_dictionary = {1: [2], 2: [1, 3], 4: [4]}
        >>> tfm.remix(remix_dictionary)

        '''
        if not (isinstance(remix_dictionary, dict) or
                remix_dictionary is None):
            raise ValueError("remix_dictionary must be a dictionary or None.")

        if remix_dictionary is not None:

            if not all([isinstance(i, int) and i > 0 for i
                        in remix_dictionary.keys()]):
                raise ValueError(
                    "remix dictionary must have positive integer keys."
                )

            if not all([isinstance(v, list) for v
                        in remix_dictionary.values()]):
                raise ValueError("remix dictionary values must be lists.")

            for v_list in remix_dictionary.values():
                if not all([isinstance(v, int) and v > 0 for v in v_list]):
                    raise ValueError(
                        "elements of remix dictionary values must "
                        "be positive integers"
                    )

        if not ((isinstance(num_output_channels, int) and
                 num_output_channels > 0) or num_output_channels is None):
            raise ValueError(
                "num_output_channels must be a positive integer or None."
            )

        effect_args = ['remix']
        if remix_dictionary is None:
            effect_args.append('-')
        else:
            if num_output_channels is None:
                num_output_channels = max(remix_dictionary.keys())

            for channel in range(1, num_output_channels + 1):
                if channel in remix_dictionary.keys():
                    out_channel = ','.join(
                        [str(i) for i in remix_dictionary[channel]]
                    )
                else:
                    out_channel = '0'

                effect_args.append(out_channel)

        self.effects.extend(effect_args)
        self.effects_log.append('remix')

        return self