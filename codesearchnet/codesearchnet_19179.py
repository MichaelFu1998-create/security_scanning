def set_name_lists(ethnicity=None):
    """Set three globally available lists of names."""
    if not ethnicity: ethnicity = random.choice(get_ethnicities())
    print("Loading names from: " + ethnicity)
    filename = names_dir + ethnicity + '.json'

    try:
        with open(filename, 'r') as injson:
            data = json.load(injson)
    except:
        return 'Unable to read from file: ' + filename
    else:
        names = [ tuple(name.split(',')) for name in data ]
        random.shuffle(names)

        global female_names
        female_names = [name for name,gender,*desc in names if gender == 'girl']

        global male_names
        male_names = [name for name,gender,*desc in names if gender == 'boy']

        global nb_names
        nb_names = [name for name,gender,*desc in names if gender == 'boygirl']