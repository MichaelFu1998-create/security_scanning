def save_variables(filename, variables):
        """Save given variables in a file.
        Valid extensions: '.pyshelf' or '.shelf' (Python shelve)
                          '.mat' (Matlab archive),
                          '.hdf5' or '.h5' (HDF5 file)

        Parameters
        ----------
        filename: str
            Output file path.

        variables: dict
            Dictionary varname -> variable

        Raises
        ------
        ValueError: if the extension of the filesname is not recognized.
        """
        ext = get_extension(filename).lower()
        out_exts = {'.pyshelf', '.shelf', '.mat', '.hdf5', '.h5'}

        output_file = filename
        if not ext in out_exts:
            output_file = add_extension_if_needed(filename, '.pyshelf')
            ext = get_extension(filename)

        if ext == '.pyshelf' or ext == '.shelf':
            save_variables_to_shelve(output_file, variables)

        elif ext == '.mat':
            save_variables_to_mat(output_file, variables)

        elif ext == '.hdf5' or ext == '.h5':
            from .hdf5 import save_variables_to_hdf5
            save_variables_to_hdf5(output_file, variables)

        else:
            raise ValueError('Filename extension {0} not accepted.'.format(ext))