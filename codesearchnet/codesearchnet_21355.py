def add_tag():
    """
        Obtains the data from the pipe and appends the given tag.
    """
    if len(sys.argv) > 1:
        tag = sys.argv[1]
        doc_mapper = DocMapper()
        if doc_mapper.is_pipe:
            count = 0
            for obj in doc_mapper.get_pipe():
                obj.add_tag(tag)
                obj.update(tags=obj.tags)
                count += 1
            print_success("Added tag '{}' to {} object(s)".format(tag, count))
        else:
            print_error("Please use this script with pipes")
    else:
        print_error("Usage: jk-add-tag <tag>")
        sys.exit()