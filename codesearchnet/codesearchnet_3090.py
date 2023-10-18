def translate_func(name, block, args):
    """Translates functions and all nested functions to Python code.
       name -  name of that function (global functions will be available under var while
            inline will be available directly under this name )
       block - code of the function (*with* brackets {} )
       args - arguments that this function takes"""
    inline = name.startswith('PyJsLvalInline')
    real_name = ''
    if inline:
        name, real_name = name.split('@')
    arglist = ', '.join(args) + ', ' if args else ''
    code = '@Js\ndef %s(%sthis, arguments, var=var):\n' % (name, arglist)
    # register local variables
    scope = "'this':this, 'arguments':arguments"  #it will be a simple dictionary
    for arg in args:
        scope += ', %s:%s' % (repr(arg), arg)
    if real_name:
        scope += ', %s:%s' % (repr(real_name), name)
    code += indent('var = Scope({%s}, var)\n' % scope)
    block, nested_hoisted, nested_inline = remove_functions(block)
    py_code, to_register = translate_flow(block)
    #register variables declared with var and names of hoisted functions.
    to_register += nested_hoisted.keys()
    if to_register:
        code += indent('var.registers(%s)\n' % str(to_register))
    for nested_name, info in nested_hoisted.iteritems():
        nested_block, nested_args = info
        new_code = translate_func('PyJsLvalTempHoisted', nested_block,
                                  nested_args)
        # Now put definition of hoisted function on the top
        code += indent(new_code)
        code += indent(
            'PyJsLvalTempHoisted.func_name = %s\n' % repr(nested_name))
        code += indent(
            'var.put(%s, PyJsLvalTempHoisted)\n' % repr(nested_name))
    for nested_name, info in nested_inline.iteritems():
        nested_block, nested_args = info
        new_code = translate_func(nested_name, nested_block, nested_args)
        # Inject definitions of inline functions just before usage
        # nested inline names have this format : LVAL_NAME@REAL_NAME
        py_code = inject_before_lval(py_code,
                                     nested_name.split('@')[0], new_code)
    if py_code.strip():
        code += indent(py_code)
    return code