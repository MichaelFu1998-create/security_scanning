def format_to_csv(filename, skiprows=0, delimiter=""):
    """Convert a file to a .csv file"""
    if not delimiter:
        delimiter = "\t"

    input_file = open(filename, "r")

    if skiprows:
        [input_file.readline() for _ in range(skiprows)]
 
    new_filename = os.path.splitext(filename)[0] + ".csv"
    output_file = open(new_filename, "w")

    header = input_file.readline().split()
    reader = csv.DictReader(input_file, fieldnames=header, delimiter=delimiter)
    writer = csv.DictWriter(output_file, fieldnames=header, delimiter=",")
    
    # Write header
    writer.writerow(dict((x, x) for x in header))
    
    # Write rows
    for line in reader:
        if None in line: del line[None]
        writer.writerow(line)
    
    input_file.close()
    output_file.close()
    print "Saved %s." % new_filename