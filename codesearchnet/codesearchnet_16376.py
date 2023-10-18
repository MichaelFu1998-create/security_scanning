async def get_parameters(self, parameters=None):
        """Get the settings for the requested component(s) of QTM in XML format.

        :param parameters: A list of parameters to request.
            Could be 'all' or any combination
            of 'general', '3d', '6d', 'analog', 'force', 'gazevector', 'image'.
        :rtype: An XML string containing the requested settings.
            See QTM RT Documentation for details.
        """

        if parameters is None:
            parameters = ["all"]
        else:
            for parameter in parameters:
                if not parameter in [
                    "all",
                    "general",
                    "3d",
                    "6d",
                    "analog",
                    "force",
                    "gazevector",
                    "image",
                    "skeleton",
                    "skeleton:global",
                ]:
                    raise QRTCommandException("%s is not a valid parameter" % parameter)

        cmd = "getparameters %s" % " ".join(parameters)
        return await asyncio.wait_for(
            self._protocol.send_command(cmd), timeout=self._timeout
        )