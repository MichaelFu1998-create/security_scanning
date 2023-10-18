def new_compiler(*args, **kwargs):
    """Create a C compiler.

    :param bool silent: Eat all stdio? Defaults to ``True``.

    All other arguments passed to ``distutils.ccompiler.new_compiler``.

    """
    make_silent = kwargs.pop('silent', True)
    cc = _new_compiler(*args, **kwargs)
    # If MSVC10, initialize the compiler here and add /MANIFEST to linker flags.
    # See Python issue 4431 (https://bugs.python.org/issue4431)
    if is_msvc(cc):
        from distutils.msvc9compiler import get_build_version
        if get_build_version() == 10:
            cc.initialize()
            for ldflags in [cc.ldflags_shared, cc.ldflags_shared_debug]:
                unique_extend(ldflags, ['/MANIFEST'])
        # If MSVC14, do not silence. As msvc14 requires some custom
        # steps before the process is spawned, we can't monkey-patch this.
        elif get_build_version() == 14:
            make_silent = False
    # monkey-patch compiler to suppress stdout and stderr.
    if make_silent:
        cc.spawn = _CCompiler_spawn_silent
    return cc