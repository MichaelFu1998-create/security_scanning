def create_ingest_point(self, privateStreamName, publicStreamName):
        """
        Creates an RTMP ingest point, which mandates that streams pushed into
        the EMS have a target stream name which matches one Ingest Point
        privateStreamName.

        :param privateStreamName: The name that RTMP Target Stream Names must
            match.
        :type privateStreamName: str

        :param publicStreamName: The name that is used to access the stream
            pushed to the privateStreamName. The publicStreamName becomes the
            streams localStreamName.
        :type publicStreamName: str

        :link: http://docs.evostream.com/ems_api_definition/createingestpoint
        """
        return self.protocol.execute('createIngestPoint',
                                     privateStreamName=privateStreamName,
                                     publicStreamName=publicStreamName)