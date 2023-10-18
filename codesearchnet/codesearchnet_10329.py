def _get_template(t):
    """Return a single template *t*."""
    if os.path.exists(t):           # 1) Is it an accessible file?
         pass
    else:
         _t = t
         _t_found = False
         for d in path:              # 2) search config.path
              p = os.path.join(d, _t)
              if os.path.exists(p):
                   t = p
                   _t_found = True
                   break
         _t = os.path.basename(t)
         if not _t_found:            # 3) try template dirs
              for p in templates.values():
                   if _t == os.path.basename(p):
                        t = p
                        _t_found = True     # NOTE: in principle this could match multiple
                        break               #       times if more than one template dir existed.
         if not _t_found:            # 4) try it as a key into templates
              try:
                   t = templates[t]
              except KeyError:
                   pass
              else:
                   _t_found = True
         if not _t_found:            # 5) nothing else to try...
              raise ValueError("Failed to locate the template file {t!r}.".format(**vars()))
    return os.path.realpath(t)