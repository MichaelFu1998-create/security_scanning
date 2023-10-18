def parse(self, data: RawMessage) -> Message:
        """\
        Parses a binary protobuf message into a Message object.
        """
        try:
            return self.receiver.parse(data)
        except KeyError as err:
            raise UnknownCommandError from err
        except DecodeError as err:
            raise UnknownCommandError(f"{err}") from err