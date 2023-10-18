def Js(val, Clamped=False):
    '''Converts Py type to PyJs type'''
    if isinstance(val, PyJs):
        return val
    elif val is None:
        return undefined
    elif isinstance(val, basestring):
        return PyJsString(val, StringPrototype)
    elif isinstance(val, bool):
        return true if val else false
    elif isinstance(val, float) or isinstance(val, int) or isinstance(
            val, long) or (NUMPY_AVAILABLE and isinstance(
                val,
                (numpy.int8, numpy.uint8, numpy.int16, numpy.uint16,
                 numpy.int32, numpy.uint32, numpy.float32, numpy.float64))):
        # This is supposed to speed things up. may not be the case
        if val in NUM_BANK:
            return NUM_BANK[val]
        return PyJsNumber(float(val), NumberPrototype)
    elif isinstance(val, FunctionType):
        return PyJsFunction(val, FunctionPrototype)
    #elif isinstance(val, ModuleType):
    #    mod = {}
    #    for name in dir(val):
    #        value = getattr(val, name)
    #        if isinstance(value, ModuleType):
    #            continue  # prevent recursive module conversion
    #        try:
    #            jsval = HJs(value)
    #        except RuntimeError:
    #            print 'Could not convert %s to PyJs object!' % name
    #            continue
    #        mod[name] = jsval
    #    return Js(mod)
    #elif isintance(val, ClassType):

    elif isinstance(val, dict):  # convert to object
        temp = PyJsObject({}, ObjectPrototype)
        for k, v in six.iteritems(val):
            temp.put(Js(k), Js(v))
        return temp
    elif isinstance(val, (list, tuple)):  #Convert to array
        return PyJsArray(val, ArrayPrototype)
    # convert to typedarray
    elif isinstance(val, JsObjectWrapper):
        return val.__dict__['_obj']
    elif NUMPY_AVAILABLE and isinstance(val, numpy.ndarray):
        if val.dtype == numpy.int8:
            return PyJsInt8Array(val, Int8ArrayPrototype)
        elif val.dtype == numpy.uint8 and not Clamped:
            return PyJsUint8Array(val, Uint8ArrayPrototype)
        elif val.dtype == numpy.uint8 and Clamped:
            return PyJsUint8ClampedArray(val, Uint8ClampedArrayPrototype)
        elif val.dtype == numpy.int16:
            return PyJsInt16Array(val, Int16ArrayPrototype)
        elif val.dtype == numpy.uint16:
            return PyJsUint16Array(val, Uint16ArrayPrototype)

        elif val.dtype == numpy.int32:
            return PyJsInt32Array(val, Int32ArrayPrototype)
        elif val.dtype == numpy.uint32:
            return PyJsUint16Array(val, Uint32ArrayPrototype)

        elif val.dtype == numpy.float32:
            return PyJsFloat32Array(val, Float32ArrayPrototype)
        elif val.dtype == numpy.float64:
            return PyJsFloat64Array(val, Float64ArrayPrototype)
    else:  # try to convert to js object
        return py_wrap(val)