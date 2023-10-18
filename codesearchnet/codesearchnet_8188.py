def recurse(desc, pre='pre_recursion', post=None, python_path=None):
    """
    Depth first recursion through a dictionary containing type constructors

    The arguments pre, post and children are independently either:

    * None, which means to do nothing
    * a string, which means to use the static class method of that name on the
      class being constructed, or
    * a callable, to be called at each recursion

    Arguments:

    dictionary -- a project dictionary or one of its subdictionaries
    pre -- called before children are visited node in the recursion
    post -- called after children are visited in the recursion
    python_path -- relative path to start resolving typenames

    """
    def call(f, desc):
        if isinstance(f, str):
            # f is the name of a static class method on the datatype.
            f = getattr(datatype, f, None)
        return f and f(desc)

    # Automatically load strings that look like JSON or Yaml filenames.
    desc = load.load_if_filename(desc) or desc

    desc = construct.to_type_constructor(desc, python_path)
    datatype = desc.get('datatype')

    desc = call(pre, desc) or desc

    for child_name in getattr(datatype, 'CHILDREN', []):
        child = desc.get(child_name)
        if child:
            is_plural = child_name.endswith('s')
            remove_s = is_plural and child_name != 'drivers'
            # This is because it's the "drivers" directory, whereas
            # the others are animation, control, layout, project
            # without the s. TODO: rename drivers/ to driver/ in v4

            cname = child_name[:-1] if remove_s else child_name
            new_path = python_path or ('bibliopixel.' + cname)
            if is_plural:
                if isinstance(child, (dict, str)):
                    child = [child]
                for i, c in enumerate(child):
                    child[i] = recurse(c, pre, post, new_path)
                desc[child_name] = child
            else:
                desc[child_name] = recurse(child, pre, post, new_path)

    d = call(post, desc)
    return desc if d is None else d