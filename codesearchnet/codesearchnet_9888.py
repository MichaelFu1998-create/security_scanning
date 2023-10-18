def _get_responses_list(self, raw_output, stream):
        """Get parsed response list from string output
        Args:
            raw_output (unicode): gdb output to parse
            stream (str): either stdout or stderr
        """
        responses = []

        raw_output, self._incomplete_output[stream] = _buffer_incomplete_responses(
            raw_output, self._incomplete_output.get(stream)
        )

        if not raw_output:
            return responses

        response_list = list(
            filter(lambda x: x, raw_output.decode(errors="replace").split("\n"))
        )  # remove blank lines

        # parse each response from gdb into a dict, and store in a list
        for response in response_list:
            if gdbmiparser.response_is_finished(response):
                pass
            else:
                parsed_response = gdbmiparser.parse_response(response)
                parsed_response["stream"] = stream

                self.logger.debug("%s", pformat(parsed_response))

                responses.append(parsed_response)

        return responses