def register_custom_type(
            self, cls: type, marshaller: Optional[Callable[[Any], Any]] = default_marshaller,
            unmarshaller: Union[Callable[[Any, Any], None],
                                Callable[[Any], Any], None] = default_unmarshaller, *,
            typename: str = None, wrap_state: bool = True) -> None:
        """
        Register a marshaller and/or unmarshaller for the given class.

        The state object returned by the marshaller and passed to the unmarshaller can be any
        serializable type. Usually a dictionary mapping of attribute names to values is used.

        .. warning:: Registering marshallers/unmarshallers for any custom type will override any
            serializer specific encoding/decoding hooks (respectively) already in place!

        :param cls: the class to register
        :param marshaller: a callable that takes the object to be marshalled as the argument and
              returns a state object
        :param unmarshaller: a callable that either:

            * takes an uninitialized instance of ``cls`` and its state object as arguments and
              restores the state of the object
            * takes a state object and returns a new instance of ``cls``
        :param typename: a unique identifier for the type (defaults to the ``module:varname``
            reference to the class)
        :param wrap_state: ``True`` to wrap the marshalled state before serialization so that it
            can be recognized later for unmarshalling, ``False`` to serialize it as is

        """
        assert check_argument_types()
        typename = typename or qualified_name(cls)

        if marshaller:
            self.marshallers[cls] = typename, marshaller, wrap_state
            self.custom_type_codec.register_object_encoder_hook(self)

        if unmarshaller and self.custom_type_codec is not None:
            target_cls = cls  # type: Optional[type]
            if len(signature(unmarshaller).parameters) == 1:
                target_cls = None

            self.unmarshallers[typename] = target_cls, unmarshaller
            self.custom_type_codec.register_object_decoder_hook(self)