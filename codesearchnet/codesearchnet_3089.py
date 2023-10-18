def translate_js(js, top=TOP_GLOBAL):
    """js has to be a javascript source code.
       returns equivalent python code."""
    # Remove constant literals
    no_const, constants = remove_constants(js)
    #print 'const count', len(constants)
    # Remove object literals
    no_obj, objects, obj_count = remove_objects(no_const)
    #print 'obj count', len(objects)
    # Remove arrays
    no_arr, arrays, arr_count = remove_arrays(no_obj)
    #print 'arr count', len(arrays)
    # Here remove and replace functions
    reset_inline_count()
    no_func, hoisted, inline = remove_functions(no_arr)

    #translate flow and expressions
    py_seed, to_register = translate_flow(no_func)

    # register variables and hoisted functions
    #top += '# register variables\n'
    top += 'var.registers(%s)\n' % str(to_register + hoisted.keys())

    #Recover functions
    # hoisted functions recovery
    defs = ''
    #defs += '# define hoisted functions\n'
    #print len(hoisted) , 'HH'*40
    for nested_name, nested_info in hoisted.iteritems():
        nested_block, nested_args = nested_info
        new_code = translate_func('PyJsLvalTempHoisted', nested_block,
                                  nested_args)
        new_code += 'PyJsLvalTempHoisted.func_name = %s\n' % repr(nested_name)
        defs += new_code + '\nvar.put(%s, PyJsLvalTempHoisted)\n' % repr(
            nested_name)
    #defs += '# Everting ready!\n'
    # inline functions recovery
    for nested_name, nested_info in inline.iteritems():
        nested_block, nested_args = nested_info
        new_code = translate_func(nested_name, nested_block, nested_args)
        py_seed = inject_before_lval(py_seed,
                                     nested_name.split('@')[0], new_code)
    # add hoisted definitiond - they have literals that have to be recovered
    py_seed = defs + py_seed

    #Recover arrays
    for arr_lval, arr_code in arrays.iteritems():
        translation, obj_count, arr_count = translate_array(
            arr_code, arr_lval, obj_count, arr_count)
        py_seed = inject_before_lval(py_seed, arr_lval, translation)

    #Recover objects
    for obj_lval, obj_code in objects.iteritems():
        translation, obj_count, arr_count = translate_object(
            obj_code, obj_lval, obj_count, arr_count)
        py_seed = inject_before_lval(py_seed, obj_lval, translation)

    #Recover constants
    py_code = recover_constants(py_seed, constants)

    return top + py_code