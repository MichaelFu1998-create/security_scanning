def put(self, prop, val, op=None):  #external use!
        '''Just like in js: self.prop op= val
           for example when op is '+' it will be self.prop+=val
           op can be either None for simple assignment or one of:
           * / % + - << >> & ^ |'''
        if self.Class == 'Undefined' or self.Class == 'Null':
            raise MakeError('TypeError',
                            'Undefined and null dont have properties!')
        if not isinstance(prop, basestring):
            prop = prop.to_string().value
        if NUMPY_AVAILABLE and prop.isdigit():
            if self.Class == 'Int8Array':
                val = Js(numpy.int8(val.to_number().value))
            elif self.Class == 'Uint8Array':
                val = Js(numpy.uint8(val.to_number().value))
            elif self.Class == 'Uint8ClampedArray':
                if val < Js(numpy.uint8(0)):
                    val = Js(numpy.uint8(0))
                elif val > Js(numpy.uint8(255)):
                    val = Js(numpy.uint8(255))
                else:
                    val = Js(numpy.uint8(val.to_number().value))
            elif self.Class == 'Int16Array':
                val = Js(numpy.int16(val.to_number().value))
            elif self.Class == 'Uint16Array':
                val = Js(numpy.uint16(val.to_number().value))
            elif self.Class == 'Int32Array':
                val = Js(numpy.int32(val.to_number().value))
            elif self.Class == 'Uint32Array':
                val = Js(numpy.uint32(val.to_number().value))
            elif self.Class == 'Float32Array':
                val = Js(numpy.float32(val.to_number().value))
            elif self.Class == 'Float64Array':
                val = Js(numpy.float64(val.to_number().value))
            if isinstance(self.buff, numpy.ndarray):
                self.buff[int(prop)] = int(val.to_number().value)
        #we need to set the value to the incremented one
        if op is not None:
            val = getattr(self.get(prop), OP_METHODS[op])(val)
        if not self.can_put(prop):
            return val
        own_desc = self.get_own_property(prop)
        if is_data_descriptor(own_desc):
            if self.Class in [
                    'Array', 'Int8Array', 'Uint8Array', 'Uint8ClampedArray',
                    'Int16Array', 'Uint16Array', 'Int32Array', 'Uint32Array',
                    'Float32Array', 'Float64Array'
            ]:
                self.define_own_property(prop, {'value': val})
            else:
                self.own[prop]['value'] = val
            return val
        desc = self.get_property(prop)
        if is_accessor_descriptor(desc):
            desc['set'].call(self, (val, ))
        else:
            new = {
                'value': val,
                'writable': True,
                'configurable': True,
                'enumerable': True
            }
            if self.Class in [
                    'Array', 'Int8Array', 'Uint8Array', 'Uint8ClampedArray',
                    'Int16Array', 'Uint16Array', 'Int32Array', 'Uint32Array',
                    'Float32Array', 'Float64Array'
            ]:
                self.define_own_property(prop, new)
            else:
                self.own[prop] = new
        return val