def map(self, from_obj, to_type, ignore_case=False, allow_none=False, excluded=None):
        """Method for creating target object instance

        :param from_obj: source object to be mapped from
        :param to_type: target type
        :param ignore_case: if set to true, ignores attribute case when performing the mapping
        :param allow_none: if set to true, returns None if the source object is None; otherwise throws an exception
        :param excluded: A list of fields to exclude when performing the mapping

        :return: Instance of the target class with mapped attributes
        """
        if (from_obj is None) and allow_none:
            return None
        else:
            # one of the tests is explicitly checking for an attribute error on __dict__ if it's not set
            from_obj.__dict__

        inst = to_type()
        key_from = from_obj.__class__.__name__
        key_to = to_type.__name__

        def not_private(s):
            return not s.startswith('_')

        def not_excluded(s):
            return not (excluded and s in excluded)

        from_obj_attributes = getmembers(from_obj, lambda a: not isroutine(a))
        from_obj_dict = {k: v for k, v in from_obj_attributes
                         if not_private(k) and not_excluded(k)}

        to_obj_attributes = getmembers(inst, lambda a: not isroutine(a))
        to_obj_dict = {k: v for k, v in to_obj_attributes if not_private(k)}

        if ignore_case:
            from_props = CaseDict(from_obj_dict)
            to_props = CaseDict(to_obj_dict)
        else:
            from_props = from_obj_dict
            to_props = to_obj_dict

        for prop in to_props:
            if self.mappings is not None \
                    and key_from in self.mappings \
                    and key_to in self.mappings[key_from]:
                if prop in self.mappings[key_from][key_to]:
                    # take mapping function
                    try:
                        fnc = self.mappings[key_from][key_to][prop]
                        if fnc is not None:
                            setattr(inst, prop, fnc(from_obj))
                            # none suppress mapping
                    except Exception:
                        raise ObjectMapperException("Invalid mapping function while setting property {0}.{1}".
                                                    format(inst.__class__.__name__, prop))

                else:
                    # try find property with the same name in the source
                    if prop in from_props:
                        setattr(inst, prop, from_props[prop])
                        # case when target attribute is not mapped (can be extended)
            else:
                raise ObjectMapperException("No mapping defined for {0} -> {1}".format(key_from, key_to))

        return inst