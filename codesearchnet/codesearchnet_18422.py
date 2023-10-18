def unwrap_state_dict(self, obj: Dict[str, Any]) -> Union[Tuple[str, Any], Tuple[None, None]]:
        """Unwraps a marshalled state previously wrapped using :meth:`wrap_state_dict`."""
        if len(obj) == 2:
            typename = obj.get(self.type_key)
            state = obj.get(self.state_key)
            if typename is not None:
                return typename, state

        return None, None