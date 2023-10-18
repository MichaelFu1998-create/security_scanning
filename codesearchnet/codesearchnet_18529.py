def total_hours(input_files):
    """
    Totals the hours for a given projct. Takes a list of input files for 
    which to total the hours. Each input file represents a project.
    There are only multiple files for the same project when the duration 
    was more than a year. A typical entry in an input file might look 
    like this: 

    8/24/14
    9:30-12:00 wrote foobar code for x, wrote a unit test for foobar code, tested. 
    2.5 hours
   
    Args:
        input_files: a list of files to parse.

    Returns:
        float: the total number of hours spent on the project.
    """
    hours = 0 
    # Look for singular and plural forms of the word
    # and allow typos.
    allow = set(['hours', 'hour', 'huors', 'huor'])
    for input_file in input_files:
        doc = open(input_file, 'r')
        for line in doc:
            line = line.rstrip()
            data = line.split(' ')
            if (len(data) == 2) and (is_numeric(data[0])) and (data[1].lower() in allow):
                hours += float(data[0])
        doc.close()
    return hours