def _generate_template_dict(dirname):
    """Generate a list of included files *and* extract them to a temp space.

    Templates have to be extracted from the egg because they are used
    by external code. All template filenames are stored in
    :data:`config.templates`.
    """
    return dict((resource_basename(fn), resource_filename(__name__, dirname +'/'+fn))
                for fn in resource_listdir(__name__, dirname)
                if not fn.endswith('~'))