def modify_input():
    """
        This functions gives the user a way to change the data that is given as input.
    """
    doc_mapper = DocMapper()
    if doc_mapper.is_pipe:
        objects = [obj for obj in doc_mapper.get_pipe()]
        modified = modify_data(objects)
        for line in modified:
            obj = doc_mapper.line_to_object(line)
            obj.save()
        print_success("Object(s) successfully changed")
    else:
        print_error("Please use this tool with pipes")