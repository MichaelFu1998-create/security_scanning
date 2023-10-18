def wrap_state_dict(self, typename: str, state) -> Dict[str, Any]:
        """
        Wrap the marshalled state in a dictionary.

        The returned dictionary has two keys, corresponding to the ``type_key`` and ``state_key``
        options. The former holds the type name and the latter holds the marshalled state.

        :param typename: registered name of the custom type
        :param state: the marshalled state of the object
        :return: an object serializable by the serializer

        """
        return {self.type_key: typename, self.state_key: state}