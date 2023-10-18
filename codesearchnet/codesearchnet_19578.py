def add_flag(*args, **kwargs):
    """
    define a single flag.
    add_flag(flagname, default_value, help='', **kwargs)
    add_flag([(flagname, default_value, help), ...])
    or
    define flags without help message
    add_flag(flagname, default_value, help='', **kwargs)

    add_flag('gpu', 1, help='CUDA_VISIBLE_DEVICES')
    :param args:
    :param kwargs:
    :return:
    """
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        for a in args[0]:
            flag.add_flag(*a)
    elif args:
        flag.add_flag(*args, **kwargs)
    else:
        for f, v in kwargs.items():
            flag.add_flag(f, v)