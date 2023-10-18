def translate_array(array, lval, obj_count=1, arr_count=1):
    """array has to be any js array for example [1,2,3]
       lval has to be name of this array.
       Returns python code that adds lval to the PY scope it should be put before lval"""
    array = array[1:-1]
    array, obj_rep, obj_count = remove_objects(array, obj_count)
    array, arr_rep, arr_count = remove_arrays(array, arr_count)
    #functions can be also defined in arrays, this caused many problems since in Python
    # functions cant be defined inside literal
    # remove functions (they dont contain arrays or objects so can be translated easily)
    # hoisted functions are treated like inline
    array, hoisted, inline = functions.remove_functions(array, all_inline=True)
    assert not hoisted
    arr = []
    # separate elements in array
    for e in argsplit(array, ','):
        # translate expressions in array PyJsLvalInline will not be translated!
        e = exp_translator(e.replace('\n', ''))
        arr.append(e if e else 'None')
    arr = '%s = Js([%s])\n' % (lval, ','.join(arr))
    #But we can have more code to add to define arrays/objects/functions defined inside this array
    # translate nested objects:
    # functions:
    for nested_name, nested_info in inline.iteritems():
        nested_block, nested_args = nested_info
        new_def = FUNC_TRANSLATOR(nested_name, nested_block, nested_args)
        arr = new_def + arr
    for lval, obj in obj_rep.iteritems():
        new_def, obj_count, arr_count = translate_object(
            obj, lval, obj_count, arr_count)
        # add object definition BEFORE array definition
        arr = new_def + arr
    for lval, obj in arr_rep.iteritems():
        new_def, obj_count, arr_count = translate_array(
            obj, lval, obj_count, arr_count)
        # add object definition BEFORE array definition
        arr = new_def + arr
    return arr, obj_count, arr_count