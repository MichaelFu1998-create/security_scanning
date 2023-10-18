def add_class_methods_as_module_level_functions_for_fabric(instance, module_name, method_name, module_alias=None):
    '''
    Utility to take the methods of the instance of a class, instance,
    and add them as functions to a module, module_name, so that Fabric
    can find and call them. Call this at the bottom of a module after
    the class definition.
    '''
    import imp
    from .decorators import task_or_dryrun

    # get the module as an object
    module_obj = sys.modules[module_name]

    module_alias = re.sub('[^a-zA-Z0-9]+', '', module_alias or '')

    # Iterate over the methods of the class and dynamically create a function
    # for each method that calls the method and add it to the current module
    # NOTE: inspect.ismethod actually executes the methods?!
    #for method in inspect.getmembers(instance, predicate=inspect.ismethod):

    method_obj = getattr(instance, method_name)

    if not method_name.startswith('_'):

        # get the bound method
        func = getattr(instance, method_name)

#         if module_name == 'buildbot' or module_alias == 'buildbot':
#             print('-'*80)
#             print('module_name:', module_name)
#             print('method_name:', method_name)
#             print('module_alias:', module_alias)
#             print('module_obj:', module_obj)
#             print('func.module:', func.__module__)

        # Convert executable to a Fabric task, if not done so already.
        if not hasattr(func, 'is_task_or_dryrun'):
            func = task_or_dryrun(func)

        if module_name == module_alias \
        or (module_name.startswith('satchels.') and module_name.endswith(module_alias)):

            # add the function to the current module
            setattr(module_obj, method_name, func)

        else:

            # Dynamically create a module for the virtual satchel.
            _module_obj = module_obj
            module_obj = create_module(module_alias)
            setattr(module_obj, method_name, func)
            post_import_modules.add(module_alias)

        fabric_name = '%s.%s' % (module_alias or module_name, method_name)
        func.wrapped.__func__.fabric_name = fabric_name

        return func