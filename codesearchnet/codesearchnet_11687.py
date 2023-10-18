def populate_fabfile():
    """
    Automatically includes all submodules and role selectors
    in the top-level fabfile using spooky-scary black magic.

    This allows us to avoid manually declaring imports for every module, e.g.

        import burlap.pip
        import burlap.vm
        import burlap...

    which has the added benefit of allowing us to manually call the commands
    without typing "burlap".

    This is soley for convenience. If not needed, it can be disabled
    by specifying the environment variable:

        export BURLAP_POPULATE_STACK=0
    """
    stack = inspect.stack()
    fab_frame = None
    for frame_obj, script_fn, line, _, _, _ in stack:
        if 'fabfile.py' in script_fn:
            fab_frame = frame_obj
            break
    if not fab_frame:
        return
    try:
        locals_ = fab_frame.f_locals
        for module_name, module in sub_modules.items():
            locals_[module_name] = module
        for role_name, role_func in role_commands.items():
            assert role_name not in sub_modules, \
                ('The role %s conflicts with a built-in submodule. '
                 'Please choose a different name.') % (role_name)
            locals_[role_name] = role_func
        locals_['common'] = common

        # Put all debug commands into the global namespace.

#         for _debug_name in debug.debug.get_tasks():
#             print('_debug_name:', _debug_name)

        locals_['shell'] = shell#debug.debug.shell

        # Put all virtual satchels in the global namespace so Fabric can find them.
        for _module_alias in common.post_import_modules:
            exec("import %s" % _module_alias) # pylint: disable=exec-used
            locals_[_module_alias] = locals()[_module_alias]

    finally:
        del stack