def add_config_files_to_archive(directory, filename, config={}):
    """
    Adds configuration files to an existing archive
    """
    with zipfile.ZipFile(filename, 'a') as zip_file:
        for conf in config:
            for conf, tree in list(conf.items()):
                if 'yaml' in tree:
                    content = yaml.dump(tree['yaml'], default_flow_style=False)
                else:
                    content = tree.get('content', '')
                out("Adding file " + str(conf) + " to archive " + str(filename))
                file_entry = zipfile.ZipInfo(conf)
                file_entry.external_attr = tree.get('permissions', 0o644) << 16 
                zip_file.writestr(file_entry, content)

    return filename