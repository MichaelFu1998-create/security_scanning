def fsplit(file_to_split):
    """
        Split the file and return the list of filenames.
    """
    dirname = file_to_split + '_splitted'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    part_file_size = os.path.getsize(file_to_split) / number_of_files + 1
    splitted_files = []
    with open(file_to_split, "r") as f:
        number = 0
        actual = 0
        while 1:
            prec = actual
            # Jump of "size" from the current place in the file
            f.seek(part_file_size, os.SEEK_CUR)

            # find the next separator or EOF
            s = f.readline()
            if len(s) == 0:
                s = f.readline()
            while len(s) != 0 and s != separator:
                s = f.readline()

            # Get the current place
            actual = f.tell()
            new_file = os.path.join(dirname, str(number))

            # Create the new file
            with open(file_to_split, "r") as temp:
                temp.seek(prec)
                # Get the text we want to put in the new file
                copy = temp.read(actual - prec)
                # Write the new file
                open(new_file, 'w').write(copy)
            splitted_files.append(new_file)
            number += 1

            # End of file
            if len(s) == 0:
                break
    return splitted_files