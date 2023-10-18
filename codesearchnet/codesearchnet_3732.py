def _produce_raw_method(self):
        '''
        Returns a callable which becomes the associate or disassociate
        method for the related field.
        Method can be overridden to add additional functionality, but
        `_produce_method` may also need to be subclassed to decorate
        it appropriately.
        '''

        def method(res_self, **kwargs):
            obj_pk = kwargs.get(method._res_name)
            other_obj_pk = kwargs.get(method._other_name)
            internal_method = getattr(res_self, method._internal_name)
            return internal_method(method._relationship, obj_pk, other_obj_pk)

        return method