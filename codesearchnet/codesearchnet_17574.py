def create_template(material, path, show=False):
        """
        Create a template csv file for a data set.

        :param material: the name of the material
        :param path: the path of the directory where the file must be written
        :param show: a boolean indicating whether the created file should be \
        displayed after creation
        """
        file_name = 'dataset-%s.csv' % material.lower()
        file_path = os.path.join(path, file_name)

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Name', material])
            writer.writerow(['Description', '<Add a data set description '
                                            'here.>'])
            writer.writerow(['Reference', '<Add a reference to the source of '
                                          'the data set here.>'])
            writer.writerow(['Temperature', '<parameter 1 name>',
                            '<parameter 2 name>', '<parameter 3 name>'])
            writer.writerow(['T', '<parameter 1 display symbol>',
                             '<parameter 2 display symbol>',
                             '<parameter 3 display symbol>'])
            writer.writerow(['K', '<parameter 1 units>',
                             '<parameter 2 units>', '<parameter 3 units>'])
            writer.writerow(['T', '<parameter 1 symbol>',
                             '<parameter 2 symbol>', '<parameter 3 symbol>'])
            for i in range(10):
                writer.writerow([100.0 + i*50, float(i), 10.0 + i, 100.0 + i])

        if show is True:
            webbrowser.open_new(file_path)