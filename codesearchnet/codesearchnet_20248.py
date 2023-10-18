def push_stream(self, uri, **kwargs):
        """
        Try to push a local stream to an external destination. The pushed
        stream can only use the RTMP, RTSP or MPEG-TS unicast/multicast
        protocol.

        :param uri: The URI of the external stream. Can be RTMP, RTSP or
            unicast/multicast (d) mpegts
        :type uri: str

        :param keepAlive: If keepAlive is set to 1, the server will attempt to
            reestablish connection with a stream source after a connection has
            been lost. The reconnect will be attempted once every second
            (default: 1 true)
        :type keepAlive: int

        :param localStreamName: If provided, the stream will be given this
            name. Otherwise, a fallback techniques used to determine the stream
            name (based on the URI)
        :type localStreamName: str

        :param targetStreamName: The name of the stream at destination. If not
            provided, the target stream name willbe the same as the local
            stream name
        :type targetStreamName: str

        :param targetStreamType: It can be one of following: **live**,
            **record**, **append**. It is meaningful only for RTMP
        :type targetStreamType: str

        :param tcUrl: When specified, this value will be used to set the TC
            URL in the initial RTMP connect invoke
        :type tcUrl: str

        :param pageUrl: When specified, this value will be used to set the
            originating web page address in the initial RTMP connect invoke
        :type pageUrl: str

        :param swfUrl: When specified, this value will be used to set the
            originating swf URL in the initial RTMP connect invoke
        :type swfUrl: str

        :param ttl: Sets the IP_TTL (time to live) option on the socket
        :type ttl: int

        :param tos: Sets the IP_TOS (Type of Service) option on the socket
        :type tos: int

        :param emulateUserAgent: When specified, this value will be used as the
            user agent string. It is meaningful only for RTMP
        :type emulateUserAgent: str

        :param rtmpAbsoluteTimestamps: Forces the timestamps to be absolute
            when using RTMP.
        :type rtmpAbsoluteTimestamps: int

        :param sendChunkSizeRequest: Sets whether the RTMP stream will or will
            not send a "Set Chunk Length" message. This is significant when
            pushing to Akamai's new RTMP HD ingest point where this parameter
            should be set to 0 so that Akamai will not drop the connection.
        :type sendChunkSizeRequest: int

        :param useSourcePts: When value is true, timestamps on source inbound
            RTMP stream are passed directly to the outbound (pushed) RTMP
            streams. This affects only pushed Outbound Net RTMP with net RTMP
            source. This parameter overrides the value of the config.lua
            option of the same name.
        :type useSourcePts: int

        :link: http://docs.evostream.com/ems_api_definition/pushstream
        """
        return self.protocol.execute('pushStream', uri=uri, **kwargs)