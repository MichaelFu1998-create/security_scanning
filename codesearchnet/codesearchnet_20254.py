def transcode(self, source, destinations, **kwargs):
        """
        Changes the compression characteristics of an audio and/or video
        stream. Allows you to change the resolution of a source stream, change
        the bitrate of a stream, change a VP8 or MPEG2 stream into H.264 and
        much more. Allow users to create overlays on the final stream as well
        as crop streams.

        :param source: Can be a URI or a local stream name from EMS.
        :type source: str

        :param destinations: The target URI(s) or stream name(s) of the
            transcoded stream. If only a name is given, it will be pushed
            back to the EMS.
        :type destinations: str

        :param targetStreamNames: The name of the stream(s) at destination(s).
            If not specified, and a full URI is provided to destinations,
            name will have a time stamped value.
        :type targetStreamNames: str

        :param groupName: The group name assigned to this process. If not
            specified, groupName will have a random value.
        :type groupName: str

        :param videoBitrates: Target output video bitrate(s) (in bits/s,
            append `k` to value for kbits/s). Accepts the value `copy` to
            copy the input bitrate. An empty value passed would mean no video.
        :type videoBitrates: str

        :param videoSizes: Target output video size(s) in wxh (width x height)
            format. IE: 240x480.
        :type videoSizes: str

        :param videoAdvancedParamsProfiles: Name of video profile template
            that will be used.
        :type videoAdvancedParamsProfiles: str

        :param audioBitrates: Target output audio bitrate(s) (in bits/s,
            append `k` to value for kbits/s). Accepts the value `copy` to
            copy the input bitrate. An empty value passed would mean no audio.
        :type audioBitrates: str

        :param audioChannelsCounts: Target output audio channel(s) count(s).
            Valid values are 1 (mono), 2 (stereo), and so on. Actual supported
            channel count is dependent on the number of input audio channels.
        :type audioChannelsCounts: str

        :param audioFrequencies: Target output audio frequency(ies) (in Hz,
            append `k` to value for kHz).
        :type audioFrequencies: str

        :param audioAdvancedParamsProfiles: Name of audio profile template
            that will be used.
        :type audioAdvancedParamsProfiles: str

        :param overlays: Location of the overlay source(s) to be used. These
            are transparent images (normally in PNG format) that have the same
            or smaller size than the video. Image is placed at the top-left
            position of the video.
        :type overlays: str

        :param croppings: Target video cropping position(s) and size(s) in
            `left : top : width : height` format (e.g. 0:0:200:100. Positions
            are optional (200:100 for a centered cropping of 200 width and 100
            height in pixels). Values are limited to the actual size of the
            video.
        :type croppings: str

        :param keepAlive: If keepAlive is set to 1, the server will restart
            transcoding if it was previously activated.
        :type keepAlive: int

        :param commandFlags: Other commands to the transcode process that are
            not supported by the baseline transcode command.
        :type commandFlags: str

        :link: http://docs.evostream.com/ems_api_definition/transcode
        """
        return self.protocol.execute('transcode', source=source,
                                     destinations=destinations, **kwargs)