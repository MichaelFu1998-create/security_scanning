def pull_stream(self, uri, **kwargs):
        """
        This will try to pull in a stream from an external source. Once a
        stream has been successfully pulled it is assigned a 'local stream
        name' which can be used to access the stream from the EMS.

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

        :param forceTcp: If 1 and if the stream is RTSP, a TCP connection will
            be forced. Otherwise the transport mechanism will be negotiated
            (UDP or TCP) (default: 1 true)
        :type forceTcp: int

        :param tcUrl: When specified, this value will be used to set the TC URL
            in the initial RTMP connect invoke
        :type tcUrl: str

        :param pageUrl: When specified, this value will be used to set the
            originating web page address in the initial RTMP connect invoke
        :type pageUrl: str

        :param swfUrl: When specified, this value will be used to set the
            originating swf URL in the initial RTMP connect invoke
        :type swfUrl: str

        :param rangeStart: For RTSP and RTMP connections. A value from which
            the playback should start expressed in seconds. There are 2 special
            values: -2 and -1. For more information, please read about
            start/len parameters here:
            http://livedocs.adobe.com/flashmediaserver/3.0/hpdocs/help.html?content=00000185.html
        :type rangeStart: int

        :param rangeEnd: The length in seconds for the playback. -1 is a
            special value. For more information, please read about start/len
            parameters here:
            http://livedocs.adobe.com/flashmediaserver/3.0/hpdocs/help.html?content=00000185.html
        :type rangeEnd: int

        :param ttl: Sets the IP_TTL (time to live) option on the socket
        :type ttl: int

        :param tos: Sets the IP_TOS (Type of Service) option on the socket
        :type tos: int

        :param rtcpDetectionInterval: How much time (in seconds) should the
            server wait for RTCP packets before declaring the RTSP stream as a
            RTCP-less stream
        :type rtcpDetectionInterval: int

        :param emulateUserAgent: When specified, this value will be used as the
            user agent string. It is meaningful only for RTMP
        :type emulateUserAgent: str

        :param isAudio: If 1 and if the stream is RTP, it indicates that the
            currently pulled stream is an audio source. Otherwise the pulled
            source is assumed as a video source
        :type isAudio: int

        :param audioCodecBytes: The audio codec setup of this RTP stream if it
            is audio. Represented as hex format without '0x' or 'h'. For
            example: audioCodecBytes=1190
        :type audioCodecBytes: str

        :param spsBytes: The video SPS bytes of this RTP stream if it is video.
            It should be base 64 encoded.
        :type spsBytes: str

        :param ppsBytes: The video PPS bytes of this RTP stream if it is video.
            It should be base 64 encoded
        :type ppsBytes: str

        :param ssmIp: The source IP from source-specific-multicast. Only usable
            when doing UDP based pull
        :type ssmIp: str

        :param httpProxy: This parameter has two valid values: IP:Port - This
            value combination specifies an RTSP HTTP Proxy from which the RTSP
            stream should be pulled from Self - Specifying "self" as the value
            implies pulling RTSP over HTTP
        :type httpProxy: str

        :link: http://docs.evostream.com/ems_api_definition/pullstream
        """
        return self.protocol.execute('pullStream', uri=uri, **kwargs)