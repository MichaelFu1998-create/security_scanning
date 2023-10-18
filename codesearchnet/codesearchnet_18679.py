def load_config(filename=None, section_option_dict={}):
    """
    This function returns a Bunch object from the stated config file.

    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    NOTE:
        The values are not evaluated by default.
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    filename:
        The desired config file to read.
        The config file must be written in a syntax readable to the
        ConfigParser module -> INI syntax

        [sectionA]
        optionA1 = ...
        optionA2 = ...

    section_option_dict:
        A dictionary that contains keys, which are associated to the sections
        in the config file, and values, which are a list of the desired
        options.
        If empty, everything will be loaded.
        If the lists are empty, everything from the sections will be loaded.

    Example:
        dict = {'sectionA': ['optionA1', 'optionA2', ...],
                'sectionB': ['optionB1', 'optionB2', ...]}

        config = get_config('config.cfg', dict)
        config.sectionA.optionA1

    Other:
        Bunch can be found in configparser.py
    """

    config = ConfigParser()
    config.read(filename)

    working_dict = _prepare_working_dict(config, section_option_dict)

    tmp_dict = {}

    for section, options in working_dict.iteritems():
        tmp_dict[section] = {}
        for option in options:
            tmp_dict[section][option] = config.get(section, option)

    return Bunch(tmp_dict)